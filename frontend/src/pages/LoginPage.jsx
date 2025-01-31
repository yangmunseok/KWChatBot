import React from 'react'

const LoginPage = () => {
  return (
    <main class="flex-grow flex items-center justify-center px-4 sm:px-6 lg:px-8 py-12">
        <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-sm">
            <div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Welcome back</h2>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Please sign in to your account
                </p>
            </div>
            <form class="mt-8 space-y-6" action="#" method="POST">
                <div class="space-y-4">
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
                        <div class="mt-1 relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <i class="fas fa-envelope text-gray-400"></i>
                            </div>
                            <input id="email" name="email" type="email" required class="!rounded-button appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-custom focus:border-custom sm:text-sm text-black" placeholder="you@example.com"/>
                        </div>
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                        <div class="mt-1 relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <i class="fas fa-lock text-gray-400"></i>
                            </div>
                            <input id="password" name="password" type="password" required class="!rounded-button appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 shadow-sm placeholder-gray-400 focus:outline-none focus:ring-custom focus:border-custom sm:text-sm text-black" placeholder="••••••••"/>
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-custom focus:ring-custom border-gray-300 !rounded-button"/>
                        <label for="remember-me" class="ml-2 block text-sm text-gray-900">Remember me</label>
                    </div>
                    <div class="text-sm">
                        <a href="#" class="font-medium text-custom hover:text-custom/90">Forgot your password?</a>
                    </div>
                </div>

                <button type="submit" class="!rounded-button w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium text-white bg-custom hover:bg-custom/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-custom">
                    Sign in
                </button>

                <div class="mt-6">
                    <div class="relative">
                        <div class="absolute inset-0 flex items-center">
                            <div class="w-full border-t border-gray-300"></div>
                        </div>
                        <div class="relative flex justify-center text-sm">
                            <span class="px-2 bg-white text-gray-500">Or continue with</span>
                        </div>
                    </div>

                    <div class="mt-6 grid grid-cols-3 gap-3">
                        <button type="button" class="!rounded-button w-full inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                            <i class="fab fa-google"></i>
                        </button>
                        <button type="button" class="!rounded-button w-full inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                            <i class="fab fa-facebook-f"></i>
                        </button>
                        <button type="button" class="!rounded-button w-full inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                            <i class="fab fa-apple"></i>
                        </button>
                    </div>
                </div>
            </form>
            <p class="mt-6 text-center text-sm text-gray-600">
                Not a member?
                <span class="mx-1"></span>
                <a href="#" class="font-medium text-custom hover:text-custom/90">Create an account</a>
            </p>
        </div>
    </main> )
}

export default LoginPage