def add_points(user, points):
    if hasattr(user, "profile"):  # Safeguard against missing profiles
        user.profile.points += points
        user.profile.save()
