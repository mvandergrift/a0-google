## contacts_list

List contacts from Google Contacts. Returns contact names, email addresses, phone numbers, and organization details.

**Arguments:**
- **limit** (integer, optional): Maximum number of contacts to return. Defaults to 25.
- **sort_order** (string, optional): Sort order for contacts. One of `FIRST_NAME_ASCENDING`, `LAST_NAME_ASCENDING`, or `LAST_MODIFIED_DESCENDING`. Defaults to `FIRST_NAME_ASCENDING`.

**Examples:**

List the first 25 contacts sorted by first name:
~~~json
{
  "limit": 25
}
~~~

List contacts sorted by last name:
~~~json
{
  "limit": 50,
  "sort_order": "LAST_NAME_ASCENDING"
}
~~~

List recently modified contacts:
~~~json
{
  "limit": 10,
  "sort_order": "LAST_MODIFIED_DESCENDING"
}
~~~
