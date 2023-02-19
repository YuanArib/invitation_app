import { Outlet, Link, useLoaderData, Form, redirect, NavLink, useNavigation, } from "react-router-dom";
import { getContacts, createContact } from "../contacts";
import axios from "axios";
import React from "react";

export async function action() {
  const contact = await createContact();
  return redirect(`/contacts/${contact.id}/edit`);
}

export async function loader() {
  const contacts = await getContacts();
  return { contacts };
}

export async function api() {
  const [post, setPost] = React.useState(null);
  // axios.get('http://127.0.0.1:8000/api/template/')
  //        .then(response => {
  //           var templates = response.data;
  //           console.log(templates)
  //           return templates
  //        })
  //        .catch(error => console.error(error));}
  // React.useEffect(() => {
  //   axios.get('http://127.0.0.1:8000/api/template/').then((response) => {
  //     setPost(response.data);
  //   });
  // }, []);
}

export default function Root() {
  const [contacts, setPost] = React.useState(null);
  // const { contacts } = api();
  React.useEffect(() => {
      axios.get('http://127.0.0.1:8000/api/template/').then((response) => {
        setPost(response.data);
      });
    }, [])
  if (!contacts) return null;
  const templatelist = contacts.map(contacts => <li key={contacts.id_global} >{contacts.male_name} & {contacts.female_name} at {contacts.date}</li>);
  const navigation = useNavigation();
    return (
      <ul>{templatelist}</ul>
    );
  }