"use client";
import { useEffect, useState } from 'react';
import { generateScoreImage } from '../utils/shareUtils';

export default function TestShare() {
  const [imgSrc, setImgSrc] = useState('');

  useEffect(() => {
    generateScoreImage(99999, 'Test Game', false).then(blob => {
      setImgSrc(URL.createObjectURL(blob));
    });
  }, []);

  return (
    <div style={{ padding: '20px', background: '#000', minHeight: '100vh', display: 'flex', justifyContent: 'center' }}>
      {imgSrc ? <img src={imgSrc} style={{ height: '90vh', border: '1px solid #333' }} /> : <p style={{color: 'white'}}>Loading...</p>}
    </div>
  );
}
