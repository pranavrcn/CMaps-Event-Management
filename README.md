# CMaps

CMaps is a full-stack web application we developed with a clear goal: to connect people with local events in a simple, intuitive way. Initially designed to serve campus communities, CMaps now focuses on making event discovery and participation as seamless as possible, with a clean, minimalistic interface.

## Key Features

- **Event Discovery**: CMaps features an interactive map powered by the Google Maps API, allowing users to easily find events happening around them. 

- **Social Integration**: We implemented a social component within CMaps, enabling users to connect with friends on the platform. This feature allows for effortless event sharing and invitations, promoting a more engaged and connected community.

- **Event Filtering**: To ensure users can tailor their experience, we included filtering options by time, category, and location. This makes it simple for users to find exactly what they're interested in, enhancing their overall experience.

- **Event Details and Dashboard**: Each event has a dedicated detail page with all relevant information. Additionally, users have access to a personal dashboard where they can view saved events, popular events, and events they've created.

- **Dual Account Types**: CMaps supports two types of accounts—users and organizations. While users can discover and attend events, organizations have the tools to promote their events effectively within the campus community.

- **Scalability and Reach**: Within its first week, CMaps attracted over 500 signups and was featured in the University of Virginia Newsletter. This early traction highlighted the platform's potential and its immediate impact on the campus community.

## Technical Overview

CMaps is built with a strong focus on scalability, reliability, and user experience, using a robust stack of technologies:

- **Django**: We chose Django for the backend due to its security, scalability, and ability to handle everything from database management to routing and authentication seamlessly.
  
- **PostgreSQL**: PostgreSQL serves as our database, providing advanced features and the scalability needed to manage user data, event information, and social interactions efficiently.

- **Frontend Technologies**: The frontend is built using Bootstrap, d3.js, and jQuery, offering a responsive and user-friendly interface. Ajax is integrated for asynchronous data loading, ensuring a smooth and interactive experience.

- **Google Maps API**: We integrated the Google Maps API to power the dynamic and interactive map feature, making it easy for users to visualize events in their area.

- **Heroku**: For deployment, we used Heroku, taking advantage of its cloud platform to manage app deployment, scaling, and maintenance with minimal overhead.

## Hackathon Development

The early development of CMaps took place at the University of Virginia's HooHacks Hackathon, where it competed in the Data Science track. This experience was crucial in refining the application's direction, particularly in utilizing data to enhance event discovery and user engagement. You can learn more about this experience and our development process in our [Devpost write-up](https://devpost.com/software/cmaps).

## Strategic Partnerships and Business Decisions

During development, CMaps was in discussions for a strategic partnership with DoorList, a company also founded at the University of Virginia. DoorList had recently secured $3,000,000 in an oversubscribed seed round, and the partnership would have positioned CMaps as their public event vendor, with an API integration for our event catalog.

However, as CMaps evolved, we made the strategic decision to focus more on enhancing the campus community experience rather than expanding into public event vending. This pivot was made to stay true to CMaps' core mission and to better align with our long-term vision, resulting in the decision not to proceed with the DoorList partnership.

### Future Enhancements:

- **Enhanced Analytics**: We plan to introduce analytics tools for organizations, enabling them to better understand event engagement and optimize their promotion strategies.
- **Mobile Optimization**: Improving the mobile experience is a priority to ensure users enjoy a seamless experience across all devices.
- **Expanded Social Features**: We're considering adding more social features, such as event reviews and personalized recommendations based on user preferences.
- **University Contract**: A significant future goal for CMaps is to secure a contract with the University of Virginia, positioning the platform as the primary event management tool for the campus. This would involve surpassing the current platform, Presence, by offering a more intuitive, community-focused solution that meets the needs of students and organizations better.

