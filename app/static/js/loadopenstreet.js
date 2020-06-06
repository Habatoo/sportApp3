function GetMap(lon, lat) {
    lon = lon || 82.87524; // Москва 	37.62, 55.75
    lat = lat || 55.05954;
    map = new OpenLayers.Map("OSMap"); //инициализация карты
    var mapnik = new OpenLayers.Layer.OSM(); //создание слоя карты
    map.addLayer(mapnik); //добавление слоя
    map.zoomToMaxExtent();
    //долгота - Широта
    var lonlat = new OpenLayers.LonLat(lon, lat);
    map.setCenter(lonlat.transform(
            new OpenLayers.Projection("EPSG:4326"), // переобразование в WGS 1984
            new OpenLayers.Projection("EPSG:900913") // переобразование проекции
        ), 14 // масштаб 
    );

    // ссылка внизу карты на текущее положение/масштаб
    map.addControl(new OpenLayers.Control.Permalink());
    map.addControl(new OpenLayers.Control.Permalink('permalink'));

    map.addControl(
        new OpenLayers.Control.MousePosition({
            displayProjection: new OpenLayers.Projection('EPSG:4326')
        })
    );

    // шкала для выбора заранее настроенного масштаба
    //map.addControl(new OpenLayers.Control.PanZoomBar());

    // панель инструментов (сдвиг и масштабирование)
    //map.addControl(new OpenLayers.Control.MouseToolbar());

    var layerMarkers = new OpenLayers.Layer.Markers("Markers"); //создаем новый слой маркеров
    map.addLayer(layerMarkers); //добавляем этот слой к карте
    map.events.register('click', map, function(e) {
        var size = new OpenLayers.Size(25, 25); //размер картинки для маркера
        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h); //смещение картинки для маркера
        var icon = new OpenLayers.Icon('static/img/icons/smiles.png', size, offset); //картинка для маркера
        layerMarkers.addMarker( //добавляем маркер к слою маркеров
            new OpenLayers.Marker(map.getLonLatFromViewPortPx(e.xy), //координаты вставки маркера
                icon)); //иконка маркера
    }); //добавление событие клика по карте
}