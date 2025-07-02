from langchain.tools import tool
from hubspot import HubSpot
import os, re
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException  
from hubspot.crm.deals import SimplePublicObjectInput as DealInput
from config_loader import config

# ─── HubSpot client ────────────────────────────────────────────────
client = HubSpot(access_token= config["hubspot_api_key"])

@tool
def create_contact(info: str) -> str:
    """
    Create a HubSpot contact.

    Parameter
    ---------
    info : str   # expected "Full Name, email@example.com"

    Returns
    -------
    str : human‑readable success or error message.
    """
    try:
        # 1. Split input
        parts = [p.strip() for p in info.split(",")]
        if len(parts) != 2:
            raise ValueError(
                "Input must be in the format 'Full Name, email@example.com'"
            )
        name, email = parts
        name, email = [x.strip().strip("'").strip('"') for x in info.split(",")]
        # 2. E‑mail validation
        EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")  # basic RFC5322-ish

        if not EMAIL_RE.match(email):
            raise ValueError(f"Invalid e‑mail address: {email!r}")

        # 3. Build contact payload
        first, *rest = name.split()          # crude first/last split
        lastname = " ".join(rest) or "(blank)"

        contact_input = SimplePublicObjectInput(
            properties={
                "email": email,
                "firstname": first,
                "lastname": lastname,
            }
        )

        # 4. Call HubSpot
        client.crm.contacts.basic_api.create(contact_input)

        return f"Created contact: {name} <{email}>"

    # ── HubSpot‑specific error ─────────────────────────────────────
    except ApiException as api_err:
        # HubSpot returns JSON with status / message
        detail = getattr(api_err, "body", str(api_err))
        return f"HubSpot API error ({api_err.status}): {detail}"

    # ── Validation or other coding error ───────────────────────────
    except ValueError as ve:
        return f" Validation error: {ve}"

    except Exception as e:
        return f"Unexpected error: {e.__class__.__name__}: {e}"

@tool
def update_contact(info: str) -> str:
    """
    Update a contact in HubSpot CRM.
    
    Input format:
        'email, property_name, new_value'
        
    Example:
        "email@example.com, firstname, example Updated"
    """
    try:
        email, property_name, new_value = [x.strip().strip("'").strip('"') for x in info.split(",")]
        search_response = client.crm.contacts.search_api.do_search(
            {
                "filterGroups": [{
                    "filters": [{
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email
                    }]
                }]
            }
        )

        if not search_response.results:
            return f"No contact found with email {email}"

        contact_id = search_response.results[0].id

        properties = {property_name: new_value}
        contact_input = SimplePublicObjectInput(properties=properties)
        client.crm.contacts.basic_api.update(contact_id, simple_public_object_input=contact_input)

        return f"Contact updated: {property_name} → {new_value} for {email}"

    except Exception as e:
        return f"HubSpot update error: {str(e)}"


@tool
def create_deal(info: str) -> str:
    """
    Create a HubSpot deal.

    Input format: 'Deal Name, Amount, Stage'
    Example: 'Big Client Opportunity, 5000, appointmentscheduled'
    """
    try:
        name, amount, stage = [x.strip().strip("'").strip('"') for x in info.split(",", 2)]

        properties = {
            "dealname": name,
            "amount": amount,
            "dealstage": stage
        }
        deal_input = DealInput(properties=properties)
        result = client.crm.deals.basic_api.create(deal_input)

        return f"Deal created: {name} with amount {amount} at stage {stage}"

    except Exception as e:
        return f"Error creating deal: {str(e)}"

@tool
def update_deal(info: str) -> str:
    """
    Update a HubSpot deal.
    Input format: 'deal_id, field, value'
    Example: '123456789, amount, 5000'
    """
    try:
        deal_id, field, value = [x.strip() for x in info.split(",", 2)]

        properties = {field: value}
        deal_input = DealInput(properties=properties)
        client.crm.deals.basic_api.update(deal_id, deal_input)

        return f"Deal {deal_id} updated: {field} → {value}"
    except Exception as e:
        return f"Error updating deal: {str(e)}"