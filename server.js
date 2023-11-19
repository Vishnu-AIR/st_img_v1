// index.js
const { spawn } = require('child_process');
const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const port = 3333;
var fname ;

// Set up Multer storage
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'public/'); // Set the destination folder for uploaded files
  },
  filename: function (req, file, cb) {
    const uniqueName = Date.now() + path.extname(file.originalname).split('.')[0]+".jpg";
    cb(null, uniqueName); 
    fname = uniqueName
    // Set the filename to a unique identifier
  },
});



function callPythonFunction(image,res) {
    const pythonProcess = spawn('python3', ['new.py', image]);

    var pythonOutput ;

    pythonProcess.stdout.on('data', (data) => {
        pythonOutput = data.toString();
        console.log(pythonOutput)
        
    });

    pythonProcess.stderr.on('data', (data) => {
        
       // console.log('Python stderr: '+data);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            // Successfully executed
            //const result = pythonOutput;
            console.log("Done");
            res.json({data: pythonOutput})
            
        } else {
            console.error(`Python process exited with code ${code}`);
        }
    });

    
}


const upload = multer({ storage: storage });

// Define a route for handling file uploads
app.post('/upload', upload.single('image'), (req, res) => {
    console.log("uploading...")
    //res.json({ message: 'Image uploaded successfully!' });
  //console.log(fname);
  callPythonFunction(fname,res);
 

  
});

app.listen(port, () => {
  console.log(`Server is running on port http://localhost:${port}`);
});
