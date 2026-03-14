## contacts_create

Create a new contact in Google Contacts with name, email, phone number, and organization details.

**Arguments:**
- **first_name** (string, required): Contact's first name.
- **last_name** (string, optional): Contact's last name.
- **email** (string, optional): Contact's email address.
- **phone** (string, optional): Contact's phone number.
- **organization** (string, optional): Contact's company or organization name.
- **title** (string, optional): Contact's job title within the organization.

**Examples:**

Create a contact with all fields:
~~~json
{
  "first_name": "Alice",
  "last_name": "Johnson",
  "email": "alice.johnson@company.com",
  "phone": "+1-555-123-4567",
  "organization": "Acme Corp",
  "title": "Engineering Manager"
}
~~~

Create a minimal contact:
~~~json
{
  "first_name": "Bob",
  "email": "bob@example.com"
}
~~~

Create a contact with name and phone only:
~~~json
{
  "first_name": "Carol",
  "last_name": "Davis",
  "phone": "+44-20-7946-0958"
}
~~~
