import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState('admin'); // This would come from auth context in a real app

  const handleLogout = () => {
    // For now, just navigate to the login page
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation Header */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <span className="text-xl font-bold text-blue-600">MediTrack</span>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link to="/dashboard" className="border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Dashboard
                </Link>
                <Link to="/inventory" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Inventory
                </Link>
                <Link to="/order" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Orders
                </Link>
                {userRole === 'admin' && (
                  <Link to="/users" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                    Users
                  </Link>
                )}
              </div>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="py-10">
        <header>
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold leading-tight text-gray-900">Dashboard</h1>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div className="px-4 py-8 sm:px-0">
              <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {/* Dashboard Cards */}
                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <h3 className="text-lg font-medium text-gray-900">Inventory Status</h3>
                      <div className="mt-3 text-3xl font-semibold">120 Items</div>
                      <div className="mt-1 text-sm text-gray-500">12 items low in stock</div>
                    </div>
                    <div className="bg-gray-50 px-4 py-4 sm:px-6">
                      <Link to="/inventory" className="text-sm font-medium text-blue-600 hover:text-blue-500">
                        View all inventory →
                      </Link>
                    </div>
                  </div>

                  <div className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="px-4 py-5 sm:p-6">
                      <h3 className="text-lg font-medium text-gray-900">Recent Orders</h3>
                      <div className="mt-3 text-3xl font-semibold">24 Orders</div>
                      <div className="mt-1 text-sm text-gray-500">8 pending delivery</div>
                    </div>
                    <div className="bg-gray-50 px-4 py-4 sm:px-6">
                      <Link to="/order" className="text-sm font-medium text-blue-600 hover:text-blue-500">
                        View all orders →
                      </Link>
                    </div>
                  </div>

                  {userRole === 'admin' && (
                    <div className="bg-white overflow-hidden shadow rounded-lg">
                      <div className="px-4 py-5 sm:p-6">
                        <h3 className="text-lg font-medium text-gray-900">User Management</h3>
                        <div className="mt-3 text-3xl font-semibold">15 Users</div>
                        <div className="mt-1 text-sm text-gray-500">3 new this month</div>
                      </div>
                      <div className="bg-gray-50 px-4 py-4 sm:px-6">
                        <Link to="/users" className="text-sm font-medium text-blue-600 hover:text-blue-500">
                          Manage users →
                        </Link>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Dashboard;