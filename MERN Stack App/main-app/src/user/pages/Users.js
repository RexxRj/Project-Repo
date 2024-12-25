import React from "react";

import UsersList from "../components/UsersList";

const Users = () => {
  const USERS = [
    {
      id: "u1",
      name: "Rexx",
      image:
        "https://gratisography.com/wp-content/uploads/2024/10/gratisography-cool-cat-800x525.jpg",
      places: 3,
    },
  ];

  return <UsersList items={USERS} />;
};

export default Users;
