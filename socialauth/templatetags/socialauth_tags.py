from django import  template

register = template.Library()

@register.simple_tag
def get_calculated_username(user):
    if hasattr(user, 'openidprofile_set') and user.openidprofile_set.filter().count():
        if user.openidprofile_set.filter(is_username_valid = True).count():
            return user.openidprofile_set.filter(is_username_valid = True)[0].user.username
        else:
            from django.core.urlresolvers import  reverse
            editprof_url = reverse('socialauth_editprofile')
            return u'Anonymous User. <a href="%s">Add name</a>'%editprof_url
    else:
        return user.username


@register.simple_tag
def get_user_profile_pic(user):

    def get_profile(site_profiles):
        if site_profiles:
            profiles = site_profiles.all()
            if profiles.count():
                return profiles[0]

    facebook = get_profile(user.facebook_profiles)
    if facebook: 
        return facebook.profile_image_url

    twitter = get_profile(user.twitter_profiles)
    if twitter: 
        return twitter.profile_image_url


@register.simple_tag
def get_display_name(user):

    if user.first_name:
        return "{0} {1}".format(user.first_name, user.last_name)

    return user.username
