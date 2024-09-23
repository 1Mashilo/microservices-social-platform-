import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Main from "./main/Main";
import Products from "./admin/Products";
import ProductsCreate from "./admin/ProductsCreate";
import ProductsEdit from "./admin/ProductsEdit";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes> 
          <Route path="/" element={<Main />} /> 
          <Route path="/admin/products" element={<Products />} />
          <Route path="/admin/products/create" element={<ProductsCreate />} />
          <Route path="/admin/products/:id/edit" element={<ProductsEdit />} />
          <Route path="*" element={<div>404 Not Found</div>} /> 
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;