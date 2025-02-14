<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "gegevens_db";

// Maak een verbinding
$conn = new mysqli($servername, $username, $password, $dbname);

// Controleer de verbinding
if ($conn->connect_error) {
    die("Verbinding mislukt: " . $conn->connect_error);
}

// Ontvang gegevens uit het formulier
$voornaam = $_POST['voornaam'];
$achternaam = $_POST['achternaam'];
$geslacht = $_POST['geslacht'];
$geboortedatum = $_POST['geboortedatum'];
$email = $_POST['email'];
$stad = $_POST['stad'];
$postcode = $_POST['postcode'];
$straat = $_POST['straat'];
$huisnummer = $_POST['huisnummer'];
$bus = $_POST['bus'];

//gegevens in de database in te voegen
$sql = "INSERT INTO gebruikers (voornaam, achternaam, geslacht, geboortedatum, email, stad, postcode, straat, huisnummer, bus) 
        VALUES ('$voornaam', '$achternaam', '$geslacht', '$geboortedatum', '$email', '$stad', '$postcode', '$straat', '$huisnummer', '$bus')";

if ($conn->query($sql) === TRUE) {
    // Redirect naar succespagina
    header("Location: succes.html");
    exit();
} else {
    echo "Fout bij opslaan: " . $conn->error;
}

$conn->close();
?>
