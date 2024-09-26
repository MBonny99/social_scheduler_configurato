// Firebase config
const firebaseConfig = {
    apiKey: "YOUR_FIREBASE_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    auth.createUserWithEmailAndPassword(email, password)
        .then(userCredential => {
            console.log('User registered:', userCredential.user);
            document.getElementById('auth-container').style.display = 'none';
            document.getElementById('post-container').style.display = 'block';
        })
        .catch(error => console.error('Error registering:', error));
}

function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    auth.signInWithEmailAndPassword(email, password)
        .then(userCredential => {
            console.log('User logged in:', userCredential.user);
            document.getElementById('auth-container').style.display = 'none';
            document.getElementById('post-container').style.display = 'block';
        })
        .catch(error => console.error('Error logging in:', error));
}

function createPost() {
    const caption = document.getElementById('caption').value;
    const image = document.getElementById('image').files[0];

    // Save post data to Firebase Firestore
    db.collection('PostDaPubblicare').add({
        caption: caption,
        imageUrl: image.name,  // Here, you should handle image upload to Firebase storage
        timestamp: firebase.firestore.FieldValue.serverTimestamp(),
        userId: auth.currentUser.uid,
        instagramToken: localStorage.getItem('instagram_token')  // Assuming token is stored in local storage
    }).then(() => {
        console.log('Post created successfully!');
    }).catch(error => console.error('Error creating post:', error));
}

function getInstagramToken() {
    // Instagram OAuth flow should be implemented here
    // After receiving the token, store it
    const token = 'INSTAGRAM_ACCESS_TOKEN';  // This should be the actual token
    localStorage.setItem('instagram_token', token);
}
