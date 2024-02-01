// footer.js
import React from 'react';
import './footer.css';

const Footer = () => {
    return (
        <div className="footer">
            <div className="credit">
                The content of this website is Essilor proprietary and confidential information, which access is granted to authorized persons only. 
                The content of this website should not be provided to any outside parties in any manner that would violate Essilor's policies regarding 
                the protection of confidential information.
            </div>

            <div className="confidential">
                CONFIDENTIAL © 2024 EssilorLuxottica
            </div>
        </div>
    );
};

export default Footer;
