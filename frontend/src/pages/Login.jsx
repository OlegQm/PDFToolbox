import React, { useState, useEffect } from "react";
import bg from "../assets/font.png";
import cat from "../assets/cat.png";
import Cookies from "js-cookie";
import { useNavigate, NavLink, useLocation } from "react-router-dom";
import "./auth.css";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");
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

    const location = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        if (params.get("expired") === "true") {
            setErrorMsg("Your session has expired. Please log in again.");

            const timer = setTimeout(() => {
                setErrorMsg("");
            }, 5000);

            return () => clearTimeout(timer);
        }
    }, [location]);

    useEffect(() => {
        if (errorMsg) {
            const timer = setTimeout(() => setErrorMsg(""), 3000);
            return () => clearTimeout(timer);
        }
    }, [errorMsg]);

    const handleSubmit = async e => {
        e.preventDefault();
        setErrorMsg("");

        if (!username.trim()) {
            setErrorMsg("Please enter a username.");
            return;
        }

        if (!password.trim()) {
            setErrorMsg("Please enter a password.");
            return;
        }

        try {
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            const res = await fetch(`${BASE_URL}api/authorization/token`, {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (!res.ok) {
                setErrorMsg(data.detail || "Login failed.");
                return;
            }

            Cookies.set("access_token", data.access_token, { expires: 1 });
            Cookies.set("username", username, { expires: 1 });
            navigate("/", { replace: true });

        } catch (err) {
            console.error(err);
            setErrorMsg("Login failed. Try again later.");
        }
    };

    return (
        <div className="auth-wrapper">
            <div className="auth-container">
                <nav className="tab-nav">
                    <NavLink to="/login" className={({ isActive }) => isActive ? "tab active" : "tab"}>Login</NavLink>
                    <NavLink to="/register" className={({ isActive }) => isActive ? "tab active" : "tab"}>Register</NavLink>
                </nav>

                <div className="auth-page">
                    <h2 className="auth-title">Login</h2>

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
                                        onChange={e => setPassword(e.target.value)}
                                    />
                                </div>

                                <button type="submit">Login</button>

                                {errorMsg && (
                                    <div className="error-box">{errorMsg}</div>
                                )}
                            </form>
                        </div>

                        <div className="auth-image">
                            <img src={cat} alt="Cute cat" />
                        </div>
                    </div>

                    <p className="auth-link">
                        No account? <NavLink to="/register">Register</NavLink>
                    </p>
                </div>
            </div>
        </div>
    );
}
