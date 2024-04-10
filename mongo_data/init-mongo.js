// init-mongo.js

// Definir la base de datos y colecciones que se crearán
var dbName = 'db_surveys';
var collectionName = 'surveys';

// Crea una conexión a la base de datos 'admin' para realizar operaciones de administración
var adminDb = db.getSiblingDB('admin');

// Autentica con un usuario administrador que tenga permisos para crear bases de datos y colecciones
adminDb.auth('root', 'password');

// Crea la base de datos db_surveys
adminDb.createCollection(dbName);

// Muestra un mensaje indicando que la base de datos se ha creado
print('Base de datos ' + dbName + ' creada exitosamente en la base de datos admin');

// Usa la base de datos recién creada
var dbSurveys = db.getSiblingDB(dbName);

// Crea la colección surveys dentro de la base de datos db_surveys
dbSurveys.createCollection(collectionName);

// Muestra un mensaje indicando que la colección se ha creado
print('Colección ' + collectionName + ' creada exitosamente en la base de datos ' + dbName);
