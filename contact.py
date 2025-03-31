import streamlit as st
import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            try: return json.load(f)
            except json.JSONDecodeError: return []
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

def add_contact(name, phone, email, address):
    contacts = load_contacts()
    contacts.append({"name": name, "phone": phone, "email": email, "address": address})
    save_contacts(contacts)

def search_contact(query):
    contacts = load_contacts()
    return [c for c in contacts if query.lower() in c["name"].lower() or query in c["phone"]]

def update_contact(old_name, name, phone, email, address):
    contacts = load_contacts()
    for contact in contacts:
        if contact["name"] == old_name:
            contact.update({"name": name, "phone": phone, "email": email, "address": address})
            break
    save_contacts(contacts)

def delete_contact(name):
    contacts = load_contacts()
    updated_contacts = [c for c in contacts if c["name"] != name]
    if len(updated_contacts) < len(contacts):
        save_contacts(updated_contacts)
        return True
    return False

def main():

    st.set_page_config(page_title="Contact Book", page_icon="📞")
    
    # Custom CSS for colorful interface
    st.markdown("""
    <style>
        .header {color: #4b8bbe; font-size: 24px;}
        .sidebar .sidebar-content {background-color: #f0f2f6;}
        .stButton>button {background-color: #4CAF50; color: white;}
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {border: 1px solid #4b8bbe;}
        .stSelectbox>div>div>select {border: 1px solid #4b8bbe;}
        .success {color: #4CAF50;}
        .error {color: #f44336;}
        .info {color: #2196F3;}
        .warning {color: #ff9800;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="header"></p><h2>📞 Contact Book Application</h2>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### Menu")
        menu = ["Add Contact", "View Contacts", "Search Contact", "Update Contact", "Delete Contact"]
        choice = st.selectbox("", menu, label_visibility="collapsed")
    
    if choice == "Add Contact":
        st.markdown("### Add New Contact")
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input("Name")
            phone = st.text_input("Phone Number")
        with cols[1]:
            email = st.text_input("Email")
            address = st.text_area("Address")
        
        if st.button("Add Contact", key="add"):
            if name and phone:
                add_contact(name, phone, email, address)
                st.markdown('<p class="success">Contact added successfully!</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="error">Name and Phone Number are required!</p>', unsafe_allow_html=True)

    elif choice == "View Contacts":
        st.markdown("### Contact List")
        contacts = load_contacts()
        if contacts:
            for contact in contacts:
                with st.expander(f"📌 {contact['name']} - {contact['phone']}"):
                    st.markdown(f"📧 **Email:** {contact['email']}  \n🏠 **Address:** {contact['address']}")
        else:
            st.markdown('<p class="info">No contacts available.</p>', unsafe_allow_html=True)

    elif choice == "Search Contact":
        st.markdown("### Search Contacts")
        query = st.text_input("Enter name or phone number")
        if st.button("Search", key="search"):
            if query:
                results = search_contact(query)
                if results:
                    for contact in results:
                        with st.expander(f"🔍 {contact['name']} - {contact['phone']}"):
                            st.markdown(f"📧 **Email:** {contact['email']}  \n🏠 **Address:** {contact['address']}")
                else:
                    st.markdown('<p class="warning">No contacts found.</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="warning">Please enter a name or phone number.</p>', unsafe_allow_html=True)

    elif choice == "Update Contact":
        st.markdown("### Update Contact")
        contacts = load_contacts()
        if contacts:
            selected_name = st.selectbox("Select Contact", [c["name"] for c in contacts])
            contact = next(c for c in contacts if c["name"] == selected_name)
            
            cols = st.columns(2)
            with cols[0]:
                name = st.text_input("Name", contact["name"])
                phone = st.text_input("Phone Number", contact["phone"])
            with cols[1]:
                email = st.text_input("Email", contact["email"])
                address = st.text_area("Address", contact["address"])
            
            if st.button("Update Contact", key="update"):
                if name and phone:
                    update_contact(selected_name, name, phone, email, address)
                    st.markdown('<p class="success">Contact updated successfully!</p>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown('<p class="error">Name and Phone Number are required!</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="info">No contacts available to update.</p>', unsafe_allow_html=True)

    elif choice == "Delete Contact":
        st.markdown("### Delete Contact")
        contacts = load_contacts()
        if contacts:
            selected_name = st.selectbox("Select Contact to Delete", [c["name"] for c in contacts])
            if st.button("Delete Contact", key="delete"):
                if delete_contact(selected_name):
                    st.markdown('<p class="success">Contact deleted successfully!</p>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown('<p class="error">Failed to delete contact.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="info">No contacts available to delete.</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()