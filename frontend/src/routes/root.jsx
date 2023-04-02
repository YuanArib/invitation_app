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

// export async function api() {
//   const [post, setPost] = React.useState(null);
//   // axios.get('http://127.0.0.1:8000/api/template/')
//   //        .then(response => {
//   //           var templates = response.data;
//   //           console.log(templates)
//   //           return templates
//   //        })
//   //        .catch(error => console.error(error));}
//   // React.useEffect(() => {
//   //   axios.get('http://127.0.0.1:8000/api/template/').then((response) => {
//   //     setPost(response.data);
//   //   });
//   // }, []);
// }
function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

function list() {
  const [contacts, setPost] = React.useState(null);
  // const { contacts } = api();
  React.useEffect(() => {
      axios.get('http://127.0.0.1:8000/api/template/').then((response) => {
        setPost(response.data);
      });
    }, [])
  if (!contacts) return null
  const templatelist = contacts.map(contacts =>
      // <li className="" key={contacts.id_global} >{contacts.male_name} & {contacts.female_name} at {contacts.date}</li>
      <div key={contacts.id_global} className="group relative">
        <div className="mt-4 flex justify-between">
          <div>
            <h3 className="text-sm text-gray-700">
              <a href={contacts.id_global}>
                <span aria-hidden="true" className="absolute inset-0" />
                {contacts.male_name} & {contacts.female_name}
              </a>
            </h3>
            <p className="mt-1 text-sm text-gray-500">at {contacts.date}</p>
          </div>
          <p className="text-sm font-medium text-gray-900">{contacts.description}</p>
        </div>
      </div>
  );
  const navigation = useNavigation();
    return (
      // <ul className="block">{templatelist}</ul>
        <div className="mt-6 grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
          {templatelist}
        </div>
    );
  }
export default function Root() {
  return (
      <div></div>
  )
}