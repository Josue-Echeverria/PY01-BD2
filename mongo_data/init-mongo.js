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

dbSurveys[collectionName].insertMany([
{"id_survey": 1,
    "creator": 'aaa',
    "questions": [
        {
            "id_question": 1,
            "question_text": 'why is sisyphus happy?',
            "question_type": 'abierta'
        }
    ]
},{"id_survey": 2,
    "creator": 'aaa',
    "questions": [
        {
            "id_question": 1,
            "question_text": 'favorite color?',
            "question_type": 'eleccion simple'
        },
        {
            "id_question": 2,
            "question_text": 'state of mind?',
            "question_type": 'calificacion'
        },
        {
            "id_question": 3,
            "question_text": 'what day is today?',
            "question_type": 'eleccion multiple'
        }
    ]
},{"id_survey": 3,
    "creator": 'aaa',
    "questions": [
        {
            "id_question": 1,
            "question_text": 'why are the keys volatile?',
            "question_type": 'numericas'
        },
        {
            "id_question": 2,
            "question_text": 'is light fast?',
            "question_type": 'Sí/No'
        },
        {
            "id_question": 3,
            "question_text": 'is this a question?',
            "question_type": 'elección simple'
        }
    ]
},{"id_survey": 4,
    "creator": 'aaa',
    "questions": [
        {
            "id_question": 1,
            "question_text": 'why did the chicken crossed the road?',
            "question_type": 'calificacion'
        },
        {
            "id_question": 2,
            "question_text": 'is red a color?',
            "question_type": 'Sí/No'
        }
    ]
}])


dbSurveys.createCollection('answers');
dbSurveys['answers'].insertMany([
    {"id_survey": 1,
    "respondent": 'bbb',
    "answers": [
            {
                "id_question": 1,
                "answer": "because he is a human",
                "question_type": 'abierta'
            }
        ]
    },{"id_survey": 2,
    "respondent": 'bbb',
    "answers": [
        {
            "id_question": 1,
            "answer": 5,
            "question_type": 'eleccion simple'
        },
        {
            "id_question": 2,
            "answer": 3,
            "question_type": 'calificacion'
        },
        {
            "id_question": 3,
            "answer": [1,2,10],
            "question_type": 'eleccion multiple'
        }
        ]
    },{"id_survey": 3,
    "respondent": 'bbb',
    "answers": [
            {
                "id_question": 1,
                "answer": 5,
                "question_type": 'numericas'
            },
            {
                "id_question": 2,
                "answer": 1,
                "question_type": 'Sí/No'
            },
            {
                "id_question": 3,
                "answer": 6,
                "question_type": 'elección simple'
            }
        ]
    },{"id_survey": 4,
    "respondent": 'bbb',
    "answers": [
        {
            "id_question": 1,
            "answer": 100,
            "question_type": 'calificacion'
        },
        {
            "id_question": 2,
            "answer": 0,
            "question_type": 'Sí/No'
        }
        ]
    }]);
    