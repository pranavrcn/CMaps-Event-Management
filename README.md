** We are currently shifting the app entirely to React Native so the current website is an archive of past progress and no longer functional. We are doing this based on advice given to us at UVA Founder's Forum by Marty Weiner-- ex-CTO of Reddit.


# CMaps

CMaps is a modern, full-stack web application designed to connect people with events happening nearby, with a focus on simplicity and ease of use. Originally created for campus communities, CMaps offers a minimalistic interface that allows users to discover, save, and share events seamlessly.

## Key Features

- **Event Discovery**: Users can find events happening near them using an interactive map powered by the Google Maps API. Events are displayed visually on the map, making it easy to explore what's happening in the vicinity.
  
- **Social Integration**: CMaps allows users to friend others within the platform, making it easy to share and invite friends to events. This social aspect enhances community engagement and encourages participation.

- **Event Filtering**: Users can filter events by time, category, and location to find exactly what they're interested in. This ensures that users can tailor their experience to their preferences.

- **Event Details and Dashboard**: Each event has its own detail page with all the necessary information. Users also have access to a personal dashboard where they can see saved events, popular events, and events they have created.

- **Dual Account Types**: CMaps supports two types of accounts – users and organizations. While users can discover and attend events, organizations have the tools to promote their events to the campus community.

- **Scalability and Reach**: In its first week post-launch, CMaps received over 500 signups and was featured in the University of Virginia Newsletter, highlighting its immediate impact and popularity within the campus community.

## Technical Overview

CMaps is built using a powerful combination of technologies to ensure scalability, reliability, and a seamless user experience:

- **Django**: The backend of CMaps is powered by Django, a robust and secure Python framework that handles everything from database management to routing and authentication.
  
- **PostgreSQL**: We use PostgreSQL as our database, benefiting from its advanced features and scalability to manage user data, event information, and social interactions efficiently.

- **Frontend Technologies**: The frontend is designed with a combination of Bootstrap and jQuery, ensuring a responsive and intuitive user interface. Ajax is utilized for asynchronous data loading, providing a smooth and interactive user experience.

- **Google Maps API**: The Google Maps API is integrated to provide a dynamic and interactive map feature, enabling users to visualize events in their area easily.

- **Heroku**: CMaps is deployed on Heroku, leveraging its cloud platform to manage the app's deployment, scaling, and maintenance with minimal overhead.

## Hackathon Recognition

CMaps had an early development stage at the University of Virginia's HooHacks Hackathon, where it competed in the Data Science track. This experience was pivotal in shaping the application's direction, particularly in leveraging data to enhance event discovery and user engagement. You can read more about our hackathon experience and early development process on our [Devpost write-up](https://devpost.com/software/cmaps).

## Strategic Partnerships and Business Decisions

During its development, CMaps was in talks to enter into a strategic partnership with DoorList, a company founded at the University of Virginia, which recently raised $3,000,000 in an oversubscribed seed round of funding. The partnership envisioned CMaps serving as public event vendor for DoorList, providing an API specifically designed to integrate our event catalog with their platform.

However, as CMaps evolved, our team decided to pursue a different direction for the application, focusing more on enhancing the campus community experience rather than broad public event vending. As a result, the deal with DoorList ultimately did not move forward. This decision was made to align better with our long-term vision for CMaps and to ensure the platform's growth remained true to its original mission.

## Impact and Future Goals

CMaps has proven to be a valuable tool for campus communities, fostering connections and enhancing event participation. With over 500 signups in the first week and recognition from the University of Virginia, CMaps is poised to continue growing and serving more users.

### Future Enhancements:

- **Enhanced Analytics**: Introducing analytics tools for organizations to better understand event engagement and optimize their promotion strategies.
- **Mobile Optimization**: Further refining the mobile experience to ensure users have a seamless experience on all devices.
- **Expanded Social Features**: Adding more social features, such as event reviews and recommendations based on user preferences.
- **University Contract**: A significant future goal for CMaps is to secure a contract with the University of Virginia, positioning the platform as the primary event management tool for the campus. This would involve overtaking the current platform, Presence, by offering a more intuitive, community-focused solution that better meets the needs of students and organizations.


CMaps is not just a tool, but a community platform designed to bring people together. Whether you're a technical professional impressed by the robust architecture or a non-technical stakeholder excited by its impact, CMaps represents a successful blend of innovation, technology, and user-centric design.

