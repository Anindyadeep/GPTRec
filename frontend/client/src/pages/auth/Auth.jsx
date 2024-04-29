import React, { useState } from "react";
import "./style.css";

function Auth() {
  const [name, setName] = useState("");
  const [showWelcome, setShowWelcome] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    setShowWelcome(true);
    setTimeout(() => {
      window.location.href = "/home";
    }, 2500);
  };

  const getFirstName = () => {
    const firstName = name.split(" ")[0];
    return firstName;
  };

  return (
    <div className="auth-container">
      {showWelcome ? (
        <div className="welcome-message">Welcome {getFirstName()}!</div>
      ) : (
        <div className="box">
          <span className="border-line"></span>
          <form onSubmit={handleLogin}>
            <h2>Login</h2>
            <div className="input-box">
              <input type="text" required value={name} onChange={(e) => setName(e.target.value)}/>
              <span>Name</span>
              <i></i>
            </div>
            <input type="submit" value="Login" />
          </form>
        </div>
      )}
    </div>
  );
}

export default Auth;