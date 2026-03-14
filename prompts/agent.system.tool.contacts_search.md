## contacts_search

Search Google Contacts by name, email address, phone number, or other contact fields. Returns matching contacts with their full details.

**Arguments:**
- **query** (string, required): Search query to match against contact names, email addresses, phone numbers, and organizations.
- **limit** (integer, optional): Maximum number of results to return. Defaults to 10.

**Examples:**

Search for a contact by name:
~~~json
{
  "query": "Alice Johnson",
  "limit": 5
}
~~~

Search by email domain:
~~~json
{
  "query": "@company.com",
  "limit": 25
}
~~~

Search by organization:
~~~json
{
  "query": "Acme Corp"
}
~~~
