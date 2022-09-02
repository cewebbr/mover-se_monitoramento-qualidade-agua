"use strict";

const cacheName = "cache-sistema-de-monitoramento-v1"

self.addEventListener("install", function (e) {
	e.waitUntil(
		caches.open(cacheName).then(function (cache) {
			const filesToAdd = [
				"/",
				"../static/manifest.json",
				"../static/css/base.css",
				"../static/css/index.css",
				"../static/css/login.css",
				"../static/css/sensorDetails.css",
				"../static/css/stationDetails.css",
				'../static/img/icon/water_quality.png',
				'../static/js/linearGraphics.js',
				'../static/js/radioBarGraphics.js',
				'../static/js/sensorValues.js',
				'../static/js/station.js',
				'../static/js/thermormeterGraphics.js',
				"../static/favicons/favicon.png",
				"../static/favicons/favicon-16x16.png",
				"../static/favicons/favicon-32x32.png",
				"../static/favicons/favicon-36x36.png",
				"../static/favicons/favicon-48x48.png",
				"../static/favicons/favicon-72x72.png",
				"../static/favicons/favicon-96x96.png",
				"../static/favicons/favicon-144x144.png",
				"../static/favicons/favicon-152x152.png",
				"../static/favicons/favicon-192x192.png",
				"../static/favicons/favicon-256x256.png",
				"../static/favicons/favicon-512x512.png"
			];

			return cache.addAll(filesToAdd)
		})
	)
});

self.addEventListener("activate", function (e) {
// 	e.waitUntil(
// 		caches.keys().then(function (existingCachesNames) {
// 			return Promise.all(
// 				existingCachesNames.map(function (name) {
// 					if (name !== cacheName)
// 						return caches.delete(name)
// 				})
// 			)
// 		})
// 	)
});

self.addEventListener("fetch", function (e) {

	// console.log(cacheName)

	// if (e.request.url.endsWith("login/") || e.request.url.endsWith("admin/"))
	// 	e.respondWith(fetch(e.request))

	// e.respondWith(
	// 	caches.match(e.request).then(function (recurso) {
	// 		if (recurso)
	// 			return recurso
	// 		else
	// 			return fetch(e.request).then(function (response) {
	// 				return caches.open(cacheName).then(function (cache) {
	// 					cache.put(e.request, response.clone())
	// 					return response
	// 				})
	// 			})
	// 	})
	// )
});