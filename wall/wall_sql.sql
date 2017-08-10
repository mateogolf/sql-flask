SELECT users.first_name, users.last_name, messages.* from users
JOIN messages ON users.id = messages.users_id;

SELECT users.first_name, users.last_name, comments.* from users
JOIN comments ON users.id = comments.user_id;