document.addEventListener('DOMContentLoaded', function () {
  if (document.querySelectorAll('#map').length > 0) {
    var lang = 'en';
    if (document.querySelector('html').lang) {
        lang = document.querySelector('html').lang;
    }

    var script = document.createElement('script');
    var googlemap_key = document.getElementById('googlemap_key').value;
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?key=' + googlemap_key + '&callback=initMap&&language=' + lang;
    document.getElementsByTagName('head')[0].appendChild(script);
  }
});

var TIME_SPAN_LINE_SEPARATION = 120000;

var map = null;
var latest_marker = null;
var trace_paths = [];

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: new google.maps.LatLng(36.22401833333333, 138.523035),
    zoom: 12
  });

  map.data.setStyle(function(feature) {
      //var title = feature.getProperty('datetime');
      var value = feature.getProperty('num_of_satellites');
      var value2 = feature.getProperty('report_type');
      var value3 = feature.getProperty('status');
      var title = feature.getProperty('datetime') + ', ' + value + ', ' + value2 + ', ' + value3;
      return {
          icon: getCircle(value, value2, value3),
          title: title
      };
  });
}

function getCircle(value, value2, value3) {
    return {
        path: google.maps.SymbolPath.CIRCLE,
        fillColor: 'red',
        fillOpacity: .2 * value2,
        scale: value * 4,
        strokeColor: 'black',
        strokeWeight: .5 * value3
    }
}

var color_index = ['#FF0000', '#00FF00', '#0000FF', '#888888', '#000000'];

function setPolyline(map, line, index) {
    var path = new google.maps.Polyline({
       path: line,
        geodesic: true,
        strokeColor: color_index[index % 5],
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    path.setMap(map);
}

function generateLines(map, geoJson) {
    var line = [];
    var pre_feature_datetime = null;
    var pre_feature_coordinate = null;
    var weight = 0;
    var features = geoJson['features'];
    for (var index in features) {
        // ToDo: loop の書き方、javascript 的には良くないようだ
        var feature = features[index];
        var datetime = Date.parse(feature['properties']['datetime']);
        if ((pre_feature_datetime !== null) && (datetime - pre_feature_datetime > TIME_SPAN_LINE_SEPARATION)) {
            setPolyline(map, line, weight);
            trace_paths.push(line);
            line = [];

            weight++;
        }

        var coordinates = feature['geometry']['coordinates'];

        // とどまっている場合、同じ緯度経度で記録がされつづけ、
        // Polygon の終点と次の始点がダブる可能性が高いので、
        // 同じ緯度経度は Polygon 用としてはスルーする
        if (((pre_feature_coordinate !== null) &&
                (pre_feature_coordinate[1] !== coordinates[1])) &&
            (pre_feature_coordinate[0] !== coordinates[0])) {
            line.push({lat: coordinates[1], lng: coordinates[0]});
        }

        pre_feature_datetime = datetime;
        pre_feature_coordinate = coordinates;
    }
    setPolyline(map, line, weight);
    trace_paths.push(line);
}

function clearMarkers() {
    map.data.forEach(function (feature) {
        map.data.remove(feature);
    });

    trace_paths.forEach(function (line) {
        line.setMap(null);
    });
}

function submit() {
    var from_date = encodeURIComponent(document.getElementById("from_date").value);
    var to_date = encodeURIComponent(document.getElementById("to_date").value);

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/json/" + '?from_date=' + from_date + '&to_date=' + to_date, true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                //console.log(xhr.responseText);

                // marker,line をクリア
                clearMarkers();

                var geoJson = JSON.parse(xhr.responseText);
                map.data.addGeoJson(geoJson);

                // line
                generateLines(map, geoJson);

            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
    };

    xhr.send(null);
}

function latest_submit() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/json/latest", true);
    xhr.onload = function (e) {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                //console.log(xhr.responseText);

                if (latest_marker !== null) {
                    latest_marker.setMap(null);
                }

                var latest_geoJson = JSON.parse(xhr.responseText);
                //console.log(latest_geoJson);
                var coor = latest_geoJson['features'][0]['geometry']['coordinates'];
                latest_marker = new google.maps.Marker({
                    map: map,
                    draggable: false,
                    animation: google.maps.Animation.DROP,
                    position: {lat: coor[1], lng: coor[0]}
                });

            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
    };

    xhr.send(null);
}

/* html 内ではなく、ここでイベント処理を登録しているのは、この script が defer 指定され、このファイルに
 * 書いた function の呼び出しは、呼ばれる前のファイルからはできないから
 */
var button = document.getElementById("button");
button.onclick = submit;

var latest_button = document.getElementById("latest_button");
latest_button.onclick = latest_submit;