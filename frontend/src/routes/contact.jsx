import { Form, useLoaderData } from "react-router-dom";
import { getContact } from "../contacts";
// import { templateList } from "../api";
import axios from "axios";

export async function loader({ params }) {
  return getContact(params.contactId);
}

export default function Contact() {
  function api() {axios.get('http://127.0.0.1:8000/api/template/')
         .then(response => {
            var templates = response.data;
            console.log(templates)
            return templates
         })
         .catch(error => console.error(error));}
  const templates = api()

  // const contact = {
  //   first: "Your",
  //   last: "Name",
  //   avatar: "https://placekitten.com/g/200/200",
  //   twitter: "your_handle",
  //   notes: "Some notes",
  //   favorite: true,
  // };

  return (
    <div id="contact">
      <div>
        <img
          key={templates.img}
          src={templates.img || null}
        />
      </div>

      <div>
        <h1>
          {templates.male_name || contact.female_name ? (
            <>
              {contact.first} {contact.last}
            </>
          ) : (
            <i>No Name</i>
          )}{" "}
          <Favorite contact={contact} />
        </h1>

        {contact.twitter && (
          <p>
            <a
              target="_blank"
              href={`https://twitter.com/${contact.twitter}`}
            >
              {contact.twitter}
            </a>
          </p>
        )}

        {contact.notes && <p>{contact.notes}</p>}

        <div>
          <Form action="edit">
            <button type="submit">Edit</button>
          </Form>
          <Form
            method="post"
            action="destroy"
            onSubmit={(event) => {
              if (
                !confirm(
                  "Please confirm you want to delete this record."
                )
              ) {
                event.preventDefault();
              }
            }}
          >
            <button type="submit">Delete</button>
          </Form>
        </div>
      </div>
    </div>
  );
}

function Favorite({ contact }) {
  // yes, this is a `let` for later
  let favorite = contact.favorite;
  return (
    <Form method="post">
      <button
        name="favorite"
        value={favorite ? "false" : "true"}
        aria-label={
          favorite
            ? "Remove from favorites"
            : "Add to favorites"
        }
      >
        {favorite ? "★" : "☆"}
      </button>
    </Form>
  );
}