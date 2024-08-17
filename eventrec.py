import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count, Avg, Sum
from .models import Event, UserAnalytics, User

def get_event_vector(event, vectorizer):
    """
    Converts event description and tags into a vector using TF-IDF.
    """
    combined_text = f"{event.description} {event.tags}"
    return vectorizer.transform([combined_text])

def get_user_interaction_score(user, event):
    """
    Calculates the interaction score for a user-event pair based on user analytics.
    """
    weights = {
        'attendance': 1.0,
        'save': 0.7,
        'view': 0.3
    }
    interactions = UserAnalytics.objects.filter(user=user, event=event)
    score = sum([weights[interaction.interaction_type] * interaction.interaction_value for interaction in interactions])
    return score

def recommend_events(user):
    """
    Recommends events for the given user based on content-based filtering and collaborative filtering.
    """
    # Get all events and vectorize their descriptions and tags
    events = Event.objects.all()
    descriptions = [f"{event.description} {event.tags}" for event in events]
    
    vectorizer = TfidfVectorizer()
    event_vectors = vectorizer.fit_transform(descriptions)
    
    # Calculate content-based recommendation scores
    user_interactions = UserAnalytics.objects.filter(user=user)
    if not user_interactions.exists():
        return events.order_by('-date')[:10]  # Fallback to most recent events if no interactions

    user_scores = {}
    for event in events:
        # Get the vector for the event
        event_vector = get_event_vector(event, vectorizer)
        
        # Calculate the interaction score
        interaction_score = get_user_interaction_score(user, event)
        
        # Calculate similarity with user's past interactions
        past_event_vectors = [get_event_vector(e.event, vectorizer) for e in user_interactions]
        similarity_scores = cosine_similarity(event_vector, past_event_vectors)
        
        # Combine the interaction score with similarity score
        content_score = np.mean(similarity_scores) * interaction_score
        user_scores[event] = content_score

    # Rank events based on their combined score
    recommended_events = sorted(user_scores, key=user_scores.get, reverse=True)
    
    # Collaborative filtering (using a simplified approach)
    similar_users = User.objects.annotate(
        similar_interactions=Count('useranalytics__event', filter=models.Q(useranalytics__event__in=user_interactions.values_list('event', flat=True)))
    ).exclude(id=user.id).order_by('-similar_interactions')
    
    collab_recs = []
    for similar_user in similar_users:
        similar_user_interactions = UserAnalytics.objects.filter(user=similar_user)
        collab_recs.extend([interaction.event for interaction in similar_user_interactions if interaction.event not in recommended_events])
    
    combined_recommendations = recommended_events + collab_recs
    return combined_recommendations[:10]  # Return top 10 recommended events

# Integrate into a Django view
from django.shortcuts import render

def event_recommendations_view(request):
    user = request.user
    recommended_events = recommend_events(user)
    return render(request, 'event_recommendations.html', {'events': recommended_events})
