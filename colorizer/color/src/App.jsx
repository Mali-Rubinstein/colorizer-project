import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [resultUrl, setResultUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    let uploadedFile = e.target.files[0];
    setFile(uploadedFile);
    setResultUrl(null);
    setPreviewUrl(URL.createObjectURL(uploadedFile));
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('image', file);

    try {
      const res = await fetch('http://localhost:5000/colorize', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('שגיאה בשרת');
      }

      const blob = await res.blob();
      setResultUrl(URL.createObjectURL(blob));
    } catch (err) {
      alert('שגיאה בשליחה לשרת');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>הפיכת תמונה משחור-לבן לצבעוני</h1>

      <div className="upload-box">
        <input type="file" onChange={handleFileChange} accept="image/*" />
      </div>

      {previewUrl && !resultUrl && (
  // רק תמונה אחת בשחור-לבן במרכז
  <div style={{ maxWidth: '320px', margin: '20px auto' }}>
    <h3>תמונה שחור-לבן</h3>
    <img src={previewUrl} alt="preview" className="grayscale" />
  </div>
)}

{previewUrl && resultUrl && (
  // אחרי שקיבלנו צבעוני, שתי תמונות בשורה
  <div className="images-row">
    <div>
      <h3>תמונה צבעונית</h3>
      <img src={resultUrl} alt="colored" />
    </div>
    <div>
      <h3>תמונה שחור-לבן</h3>
      <img src={previewUrl} alt="preview" className="grayscale" />
    </div>
  </div>
)}

      {previewUrl && !resultUrl && (
        <button onClick={handleUpload}>הפוך לצבע</button>
      )}

      {loading && <p>מעבד תמונה...</p>}
    </div>
  );
}

export default App;
