import React, { useState, useEffect } from "react";
import { useNavigate, NavLink } from "react-router-dom";

import bg from "../assets/font.png";
import cat from "../assets/cat.png";
import "./auth.css";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/";
export default function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");
    const [successMsg, setSuccessMsg] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const navigate = useNavigate();
    const [showConfirm, setShowConfirm] = useState(false);


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


    useEffect(() => {
        if (errorMsg) {
            const timer = setTimeout(() => setErrorMsg(""), 3000);
            return () => clearTimeout(timer);
        }
    }, [errorMsg]);

    const handleSubmit = async e => {
        e.preventDefault();
        setErrorMsg("");
        setSuccessMsg("");

        if (!username.trim()) {
            setErrorMsg("Please enter a username.");
            return;
        }

        if (!password.trim()) {
            setErrorMsg("Please enter a password.");
            return;
        }

        if (password.length < 6) {
            setErrorMsg("Password must be at least 6 characters long.");
            return;
        }
        if (password !== confirmPassword) {
            setErrorMsg("Passwords do not match.");
            return;
        }

        try {
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            const res = await fetch(`${BASE_URL}api/authorization/register`, {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (!res.ok) {
                setErrorMsg(data.detail || "Registration failed.");
                return;
            }


            setSuccessMsg(data.msg);
            setTimeout(() => navigate("/login"), 3000);

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

                                    />
                                </div>
                                <div className="field">
                                    <label htmlFor="password">Password:</label>
                                    <input
                                        id="password"
                                        type="password"
                                        placeholder="Password"
                                        value={password}
                                        onFocus={() => setShowConfirm(true)}
                                        onChange={e => setPassword(e.target.value)}

                                    />
                                </div>
                                {showConfirm && (
                                    <div className="field">
                                        <label htmlFor="confirmPassword">Confirm Password:</label>
                                        <input
                                            id="confirmPassword"
                                            type="password"
                                            placeholder="Confirm Password"
                                            value={confirmPassword}
                                            onChange={e => setConfirmPassword(e.target.value)}
                                        />
                                    </div>
                                )}

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
                            <img src={cat} alt="Cute cat"/>
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
