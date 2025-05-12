import React, { useState, useEffect } from "react";
import { useNavigate, NavLink } from "react-router-dom";

import bg from "./font.png";
import cat from "./cat.png";
import "./auth.css";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
export default function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");
    const [successMsg, setSuccessMsg] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        Object.assign(document.body.style, {
            backgroundImage: `url(${bg})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100vh",
            margin: "0"
        });
        return () => Object.assign(document.body.style, {
            backgroundImage: "",
            backgroundSize: "",
            backgroundPosition: "",
            backgroundRepeat: "",
            display: "",
            alignItems: "",
            justifyContent: "",
            height: "",
            margin: ""
        });
    }, []);

    const handleSubmit = async e => {
        e.preventDefault();
        setErrorMsg("");
        setSuccessMsg("");

        try {
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            const res = await fetch(`${BASE_URL}/api/authorization/register`, {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (!res.ok) {
                setErrorMsg(data.detail || "Registration failed.");
                return;
            }


            setSuccessMsg(data.msg);
            setTimeout(() => navigate("/login"), 2000);

        } catch (err) {
            console.error(err);
            setErrorMsg("Registration failed. Try again later.");
        }
    };

    return (
        <div className="auth-wrapper">
            <div className="auth-container">
                <nav className="tab-nav">
                    <NavLink to="/login" className="tab">Login</NavLink>
                    <NavLink to="/register" className="tab active">Register</NavLink>
                </nav>

                <div className="auth-page">
                    <h2 className="auth-title">Register</h2>

                    <div className="auth-flex">
                        <div className="auth-content">
                            <form onSubmit={handleSubmit} className="auth-form">
                                <div className="field">
                                    <label htmlFor="username">Username:</label>
                                    <input
                                        id="username"
                                        type="text"
                                        placeholder="Username"
                                        value={username}
                                        onChange={e => setUsername(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className="field">
                                    <label htmlFor="password">Password:</label>
                                    <input
                                        id="password"
                                        type="password"
                                        placeholder="Password"
                                        value={password}
                                        onChange={e => setPassword(e.target.value)}
                                        required
                                    />
                                </div>

                                {errorMsg && (
                                    <div className="error-box">{errorMsg}</div>
                                )}

                                <button type="submit">Register</button>

                                {successMsg && (
                                    <div className="success-box">{successMsg}</div>
                                )}
                            </form>
                        </div>

                        <div className="auth-image">
                            <img src={cat} alt="Cute cat" />
                        </div>
                    </div>

                    <p className="auth-link">
                        Already have an account? <NavLink to="/login">Login</NavLink>
                    </p>
                </div>
            </div>
        </div>
    );
}
