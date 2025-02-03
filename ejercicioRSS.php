<?php
$url = "https://es.wikipedia.org/w/index.php?title=Folivora&action=history&feed=rss"; // Reemplaza con la URL del feed RSS
$rss = simplexml_load_file($url);

if ($rss === false) {
    die("Error al cargar el RSS");
}

foreach ($rss->channel->item as $item) {
    echo "<h3>" . $item->title . "</h3>"; // Imprime solo el título
}
?>
