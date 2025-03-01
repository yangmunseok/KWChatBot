import { useMutation, useQueryClient } from "@tanstack/react-query";
import React, { useState } from "react";

const LoginPage = () => {
  const queryClient = useQueryClient();
  const {
    mutate: loginMutation,
    isError,
    error,
  } = useMutation({
    mutationFn: async ({ username, password }) => {
      try {
        const res = await fetch("/api/auth/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
        });
        const data = await res.json();
        console.log(res);
        if (!res.ok) {
          throw new Error(
            data.detail.error || deta.error || "Something went wrong"
          );
        }
      } catch (error) {
        throw new Error(error);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["authUser"] });
    },
  });
  const [loginForm, setLoginForm] = useState({
    username: "Username",
    password: "••••••••",
  });
  const handleInputChange = (e) => {
    setLoginForm((prevState) => {
      return { ...prevState, [e.target.name]: e.target.value };
    });
  };

  return (
    <main className="flex-grow flex items-center justify-center px-4 sm:px-6 lg:px-8 py-12">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-sm">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Welcome
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Please login to your account
          </p>
        </div>
        <form
          className="mt-8 space-y-6"
          onSubmit={(e) => {
            e.preventDefault();
            loginMutation(loginForm);
          }}
        >
          <div className="space-y-4">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700"
              >
                Username
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i className="fa-solid fa-user text-gray-400"></i>
                </div>
                <input
                  id="username"
                  name="username"
                  required
                  className="!rounded-button appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-custom focus:border-custom sm:text-sm text-black"
                  placeholder={loginForm.username}
                  onChange={handleInputChange}
                />
              </div>
            </div>
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700"
              >
                Password
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i className="fa-solid fa-lock text-gray-400"></i>
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  className="!rounded-button appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-custom focus:border-custom sm:text-sm text-black"
                  placeholder={loginForm.password}
                  onChange={handleInputChange}
                />
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-custom focus:ring-custom border-gray-300 !rounded-button"
              />
              <label
                htmlFor="remember-me"
                className="ml-2 block text-sm text-gray-900"
              >
                Remember me
              </label>
            </div>
            <div className="text-sm">
              <a
                href="#"
                className="font-medium text-custom hover:text-custom/90"
              >
                Forgot your password?
              </a>
            </div>
          </div>

          <button
            type="submit"
            className="!rounded-button w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium text-white bg-custom hover:bg-custom/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-custom"
          >
            Login
          </button>
          {isError && <p className="text-sm text-red-700">{error.message}</p>}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">
                  Or continue with
                </span>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-3 gap-3">
              <button
                type="button"
                className="!rounded-button w-full inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              >
                <i className="fab fa-google"></i>
              </button>
              <button
                type="button"
                className="!rounded-button w-full inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              >
                <i className="fab fa-facebook-f"></i>
              </button>
              <button
                type="button"
                className="!rounded-button w-full inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              >
                <i className="fab fa-apple"></i>
              </button>
            </div>
          </div>
        </form>
        <p className="mt-6 text-center text-sm text-gray-600">
          Not a member?
          <span className="mx-1"></span>
          <a
            href="/signup"
            className="font-medium text-custom hover:text-custom/90"
          >
            Create an account
          </a>
        </p>
      </div>
    </main>
  );
};

export default LoginPage;
