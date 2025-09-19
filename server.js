const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware to parse JSON request bodinpm startes
app.use(express.json());

// Serve static files from the React app build directory only in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static(path.join(__dirname, 'password', 'build')));
}

// Proxy API requests to the backend server
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:5000', // Assuming backend API is on port 5000
  changeOrigin: true,
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.status(500).send('Proxy error');
  },
}));

// Catch all handler: send back React's index.html file for client-side routing (only in production)
if (process.env.NODE_ENV === 'production') {
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'password', 'build', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
