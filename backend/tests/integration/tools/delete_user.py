def delete_user(user_id, session, base_url):
    #delete created user after
    response = session.delete(f"{base_url}/users/delete/{user_id}")