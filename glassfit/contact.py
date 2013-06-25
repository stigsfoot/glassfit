from apiclient import errors
import logging

def insert_contact(service, contact_id, display_name, icon_url):
  """Insert a new contact for the current user.

  Args:
    service: Authorized Mirror service.
    contact_id: ID of the contact to insert.
    display_name: Display name for the contact to insert.
    icon_url: URL of the contact's icon.
  Returns:
    The inserted contact on success, None otherwise.
  """
  contact = {
      'id': contact_id,
      'displayName': display_name,
      'imageUrls': [icon_url]
  }
  try:
    service.contacts().insert(body=contact).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return None


def create_contact(service):
    logging.info("Verifying that user has glassfit contact")
    contact_id = "glassfit"
    icon_url = "http://i.imgur.com/NTvzAkj.png"
    try: 
        insert_contact(service, contact_id, contact_id, icon_url)
    except errors.HttpError:
        logging.info("Failed to create glassfit contact")
