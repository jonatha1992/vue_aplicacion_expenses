import axios from "axios";
import {
  auth,
  googleProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "./firebase";

const backendAPI = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Registro con email. Se usa la contraseña para Firebase y también se envía al backend.
export const registerWithEmail = async (email, password, displayName) => {
  const result = await createUserWithEmailAndPassword(auth, email, password);
  const user = result.user;
  const payload = { username: displayName, email: user.email, password }; // En backend se debe procesar esta info
  await backendAPI.post("/register", payload);
  return user;
};

// Login con email.
export const loginWithEmail = async (email, password) => {
  const result = await signInWithEmailAndPassword(auth, email, password);
  const user = result.user;
  // Opcional: enviar al backend si se requiere crear sesión
  
  return user;
};

// Login con Google. Se registra/inicia sesión en Firebase y se manda la info al backend.
export const signInWithGoogle = async () => {
  const result = await signInWithPopup(auth, googleProvider);
  console.log("respuesta de google signInWithGoogle: ", result);
  const user = result.user;
  const payload = {
    username: user.displayName,
    email: user.email,
    password: user.uid,
  };
  await backendAPI.post("/register", payload);
  return user;
};
