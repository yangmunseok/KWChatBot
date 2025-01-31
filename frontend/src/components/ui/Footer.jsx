import React from 'react'
const Footer = () => {
  return (
    <footer class="bg-gray-900 text-white py-16">
        <div class="max-w-8xl mx-auto px-6">
            <div class="grid md:grid-cols-3 gap-12">
                <div class="space-y-6">
                    <h4 class="text-lg font-semibold">KW</h4>
                    <p class="text-gray-400">Redefining Communication with AI.</p>
                </div>
                <div class="space-y-6">
                    <h4 class="text-lg font-semibold">Quick Links</h4>
                    <ul class="space-y-4">
                        <li><a href="#" class="text-gray-400 hover:text-white">About Us</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white">Features</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white">Pricing</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white">Contact</a></li>
                    </ul>
                </div>
                <div class="space-y-6">
                    <h4 class="text-lg font-semibold">Connect With Us</h4>
                    <div class="flex space-x-4">
                        <a href="#" class="text-gray-400 hover:text-white text-xl"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="text-gray-400 hover:text-white text-xl"><i class="fab fa-linkedin"></i></a>
                        <a href="#" class="text-gray-400 hover:text-white text-xl"><i class="fab fa-facebook"></i></a>
                        <a href="#" class="text-gray-400 hover:text-white text-xl"><i class="fab fa-instagram"></i></a>
                    </div>
                </div>
            </div>
        </div>
    </footer>
  )
}

export default Footer