"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Register() {
  const router = useRouter();

  const manejarRedireccion = () => {
    router.push("/login"); // También puedes usar replace() en lugar de push()
  };

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [first_name, setFirstName] = useState("");
  const [last_name, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [birth_date, setBirthDate] = useState("");

  function read(value: string, setValue: (value: string) => void) {
    setValue(value);
  }

  const onSubmit = async () => {
    console.log("enviando data");
    const data = {
      username: username,
      password: password,
      first_name: first_name,
      last_name: last_name,
      email: email,
      birth_date: birth_date,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/users/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Error en la solicitud");
      }
      const result = await response.json();
      console.log(result);
      manejarRedireccion();
    } catch (error) {
      console.log("Error : ", error);
    }
  };

  return (
    <div>
      <div className="flex flex-col gap-3 justify-center items-center">
        <input
          className="border border-blue-500 rounded-full p-3"
          type="text"
          placeholder="User Name"
          onChange={(e) => {
            read(e.target.value, setUsername);
          }}
        />
        <input
          className="border border-blue-500 rounded-full p-3"
          type="Password"
          placeholder="Password"
          onChange={(e) => {
            read(e.target.value, setPassword);
          }}
        />
        <input
          className="border border-blue-500 rounded-full p-3"
          type="text"
          placeholder="First name"
          onChange={(e) => {
            read(e.target.value, setFirstName);
          }}
        />
        <input
          className="border border-blue-500 rounded-full p-3"
          type="text"
          placeholder="Last Name"
          onChange={(e) => {
            read(e.target.value, setLastName);
          }}
        />
        <input
          className="border border-blue-500 rounded-full p-3"
          type="email"
          placeholder="Email"
          onChange={(e) => {
            read(e.target.value, setEmail);
          }}
        />
        <input
          className="border border-blue-500 rounded-full p-3"
          type="date"
          placeholder="Fecha de Nacimiento yyyy-mm-dd"
          onChange={(e) => {
            read(e.target.value, setBirthDate);
          }}
        />
        <button
          onClick={onSubmit}
          className="border border-white rounded-lg w-50 p-3 cursor-pointer"
        >
          Register
        </button>
      </div>
    </div>
  );
}
