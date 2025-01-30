# Online Forum for Gamers

## Overview
The Online Forum for Gamers is a platform where gamers can register, log in, create posts, reply to discussions, join teams, and send private messages. The forum allows users to search for posts, like content, and manage their accounts by changing their passwords.

## Features

- **User Registration**: Users can register by providing their email, password, and role (gamer).
- **Login**: Users can log in to their account and access their posts and replies.
- **Create Post**: Users can create new posts on various topics of interest.
- **Reply to Post**: Users can reply to existing posts to contribute to discussions.
- **View Posts**: Users can view posts created by other gamers.
- **Search Posts**: Users can search for posts using keywords or categories.
- **Like Post**: Users can like posts that they find useful or interesting.
- **Join a Team**: Users can join a team or group within the forum for collaborative gameplay.
- **Send Private Message**: Users can send private messages to other forum members.
- **Change Password**: Users can change their password for added security.

## Models

- **User Model**
  - `user_id`: Unique identifier for the user.
  - `email`: User’s email address (unique).
  - `password`: Hashed password for authentication.
  - `role`: Role of the user (e.g., "gamer").

- **Post Model**
  - `post_id`: Unique identifier for the post.
  - `user`: Foreign key to the User model, indicating the author of the post.
  - `title`: Title of the post.
  - `content`: Content of the post.
  - `created_at`: Timestamp of when the post was created.

- **Team Model**
  - `team_id`: Unique identifier for the team.
  - `name`: Name of the team.
  - `description`: Description of the team.
  - `members`: Many-to-many relationship with the User model, representing the members of the team.

- **Message Model**
  - `message_id`: Unique identifier for the message.
  - `sender`: Foreign key to the User model, indicating the sender.
  - `receiver`: Foreign key to the User model, indicating the receiver.
  - `content`: Content of the message.
  - `sent_at`: Timestamp of when the message was sent.

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLAlchemy (or another ORM)
- SQLite (or any other supported database)

### Steps

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. Install dependencies using pipenv:

    ```bash
    pipenv install
    ```

3. Set up the database:

    ```bash
    pipenv run flask db upgrade
    ```

4. Run the application:

    ```bash
    pipenv run flask run
    ```

### API Endpoints

- **POST /register**: Register a new user.
- **POST /login**: Log in to an existing account.
- **GET /posts**: Get all posts.
- **POST /posts**: Create a new post.
- **GET /posts/{post_id}**: View a single post.
- **POST /posts/{post_id}/reply**: Reply to a post.
- **GET /search**: Search posts by keywords.
- **POST /posts/{post_id}/like**: Like a post.
- **POST /team/join**: Join a team.
- **POST /message/send**: Send a private message.
- **POST /change-password**: Change the user's password.

## Testing

You can test the backend using Postman or any API testing tool. Ensure that you are sending the correct headers for authentication (JWT tokens) when required.

## License

This project is licensed under the MIT License.
