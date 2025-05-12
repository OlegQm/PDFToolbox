import React, { useState, useEffect } from "react";
import bg from "./font.png";
import cat from "./cat.png";
import Cookies from "js-cookie";
import { useNavigate, NavLink, useLocation } from "react-router-dom";
import "./auth.css";

const BASE_URL = import.meta.env.VITE_BASE_URL || "http://localhost:8000";



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

            return () => clearTimeout(timer); // на случай, если компонент размонтируется
        }
    }, [location]);
    const handleSubmit = async e => {
        e.preventDefault();
        setErrorMsg(""); // сбросить прошлую ошибку

        try {
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            ////ЧУВАКИ Я ХЗ ЧТО СЮДА ПОДСТАВЛЯТЬ! ПРИ ЛОКАЛЬНОМ - ОК ФУНГУЕ - ЧТО ДЕЛАТЬ В СЛУЧАЕ С САЙТОМ - ХЗ
            const res = await fetch(`${BASE_URL}/api/authorization/token`, {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (!res.ok) {
                setErrorMsg(data.detail || "Login failed.");
                return;
            }

            // ✅ Успешный логин — сохранить токен
            Cookies.set("access_token", data.access_token, { expires: 1 }); // expires = 1 день
            navigate("/app");

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
