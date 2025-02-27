import {
  auth,
  googleProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "./firebase";
import { createAPI } from "./apiConfig";

const api = createAPI();

// Registro con email. Se usa la contraseña para Firebase y también se envía al backend.
export const registerWithEmail = async (email, password, displayName) => {
  try {
    // First register with Firebase
    const firebaseResult = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    );
    const firebaseUser = firebaseResult.user;

    console.log("datos de form user:", email, password, displayName);
    // Then register with backend
    const payload = {
      username: email, // Cambiado: usar email como username para consistencia
      email: firebaseUser.email,
      password: password,
      display_name: displayName, // Agregado: enviar displayName como campo separado
    };

    // Register in backend
    await api.post("auth/register", payload);

    // After registration, we need to login to get the token
    const loginResponse = await api.post("auth/login", {
      username: email, // Cambiado: usar email como username
      email: email,
      password: password,
    });

    // Return the same structure as Google login
    return {
      user: {
        username: displayName,
        email: firebaseUser.email,
      },
      access_token: loginResponse.data.access_token,
    };
  } catch (error) {
    console.error("Error in registration:", error);
    throw error;
  }
};

// Login con email.
export const loginWithEmail = async (email, password) => {
  try {
    const firebaseResult = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );
    const firebaseUser = firebaseResult.user;

    // Hacer la petición al backend
    const backendResponse = await api.post("auth/login", {
      username: email,
      email: email,
      password: password,
    });

    // Asegurarnos de que devolvemos el objeto en el formato correcto
    return {
      user: {
        username: backendResponse.data.username,
        email: firebaseUser.email,
      },
      access_token: backendResponse.data.access_token,
    };
  } catch (error) {
    console.error("Error en login:", error);
    throw error;
  }
};

export const signInWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;

    console.log("Google user:", user);

    const payload = {
      username: user.displayName, // Usar email como username
      email: user.email,
      password: user.uid,
    };

    let backendResponse;
    try {
      // Intentar login primero
      backendResponse = await api.post("auth/login", payload);
    } catch (e) {
      if (e.response?.status === 401) {
        // Si falla el login, intentar registro
        await api.post("auth/register", payload);
        // Y luego login
        backendResponse = await api.post("auth/login", payload);
      } else {
        throw e;
      }
    }

    return {
      user: {
        username: backendResponse.data.username,
        email: user.email,
      },
      access_token: backendResponse.data.access_token,
    };
  } catch (error) {
    console.error("Error during Google sign-in:", error);
    throw error;
  }
};
