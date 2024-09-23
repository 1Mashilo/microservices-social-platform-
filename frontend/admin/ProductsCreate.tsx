import React, { SyntheticEvent, useState } from 'react';
import Wrapper from "./Wrapper";
import { useNavigate } from 'react-router-dom';

const ProductsCreate = () => {
    const [title, setTitle] = useState('');
    const [image, setImage] = useState('');
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null); 

    const submit = async (e: SyntheticEvent) => {
        e.preventDefault();

        try {
            const response = await fetch('http://backend:8000/api/products', { 
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title,
                    image
                })
            });

            if (!response.ok) { 
                const errorData = await response.json(); 
                throw new Error(errorData.message || 'Failed to create product'); 
            }

            navigate('/admin/products');
        } catch (error) {
            console.error('Error creating product:', error);
            setError('An error occurred while creating the product. Please try again.'); 
        }
    };



    return (
        <Wrapper>
            {error && <div className="alert alert-danger">{error}</div>}

            <form onSubmit={submit}>
                <div className="form-group">
                    <label>Title</label>
                    <input type="text" className="form-control" name="title"
                           onChange={e => setTitle(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label>Image</label>
                    <input type="text" className="form-control" name="image"
                           onChange={e => setImage(e.target.value)}
                    />
                </div>
                <button className="btn btn-outline-secondary">Save</button>
            </form>
        </Wrapper>
    );
};

export default ProductsCreate;