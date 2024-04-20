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

// Usa la base de datos recién creada
var dbSurveys = db.getSiblingDB(dbName);

// Crea la colección surveys dentro de la base de datos db_surveys
dbSurveys.createCollection(collectionName);

// Datos de preuba 
// Se generan las encuestas
dbSurveys[collectionName].insertMany([
{"id_survey": 1,
    "creator": 'creador',
    "name": "Testing survey",
    "description": "This is just testing survey",
    "published": true,
    "questions": [
        {
            "id_question": 1,
            "question_text": 'Why is sisyphus happy?',
            "question_type": 'abierta'
        },{
            "id_question": 2,
            "question_text": 'Is the earth flat?',
            "question_type": 'si/no'
        },{
            "id_question": 3,
            "question_text": ' Which one is better?',
            "options": ['Computer science', 'Systems engineering', 'Computer engineering'],
            "question_type": 'eleccion simple'
        },{
            "id_question": 4,
            "question_text": 'Why is docker the best virtual enviroment?',
            "question_type": 'abierta'
        },{
            "id_question": 5,
            "question_text": 'Is Linux just better?',
            "question_type": 'si/no'
        },{
            "id_question": 6,
            "question_text": 'What day is today?',
            "question_type": 'numericas'
        },{
            "id_question": 7,
            "question_text": 'would rather have unlimited bacon but no games?',
            "question_type": 'si/no'
        },{
            "id_question": 8,
            "question_text": 'Which place is better to go for vacations?',
            "options": ['The beach', 'The mountain', 'River', 'None'],
            "question_type": 'eleccion multiple'
        },{
            "id_question": 9,
            "question_text": 'How much would you rate this survey?',
            "question_type": 'calificacion'
        }

    ]
},{"id_survey": 2,
    "creator": 'creador',
    "name": "Testing survey2",
    "description": "This is just testing survey",
    "published": true,
    "questions": [
        {
            "id_question": 1,
            "question_text": "Do you like Python?",
            "question_type": "si/no"
        },
        {
            "id_question": 2,
            "question_text": "Which one is your favorite?",
            "options": ["Python", "Java", "C++", "JavaScript"],
            "question_type": "eleccion simple"
        },
        {
            "id_question":3,
            "question_text": "Is JavaScript a compiled language?",
            "question_type": "si/no"
        },
        {
            "id_question": 4,
            "question_text": "How many years of experience do you have in programming?",
            "question_type": "numericas"
        },
        {
            "id_question": 5,
            "question_text": "Would you rather work with front-end or back-end?",
            "question_type": "eleccion simple",
            "options": ["front-end", "back-end"]
        },
        {
            "id_question": 6,
            "question_text": "How much would you rate your programming skills?",
            "question_type": "calificacion"
        },
        {
            "id_question": 7,
            "question_text": "What is your favorite IDE?",
            "question_type": "abierta"
        },{
            "id_question": 8,
            "question_text": "Do you prefer cats or dogs?",
            "question_type": "si/no"
        },
        {
            "id_question": 9,
            "question_text": "Which one is your favorite pet?",
            "options": ["Dog", "Cat", "Bird", "Fish"],
            "question_type": "eleccion simple"
        },{
            "id_question": 10,
            "question_text": "How much would you rate your data analysis skills?",
            "question_type": "calificacion"
        },
        {
            "id_question": 11,
            "question_text": "How much would you rate your teamwork skills?",
            "question_type": "calificacion"
        }
    ]
    
},{"id_survey": 3,
    "creator": 'creador',
    "name": "Testing survey3",
    "description": "This is just testing survey",
    "published": true,
    "questions": [
        {
            "id_question": 1,
            "question_text": 'why are the keys volatile?',
            "question_type": 'numericas'
        },
        {
            "id_question": 2,
            "question_text": 'is light fast?',
            "question_type": 'si/no'
        },
        {
            "id_question": 3,
            "question_text": 'is this a question?',
            "options": ['Maybe', 'Yes','No','I dont know'],
            "question_type": 'eleccion simple'
        },
        {
            "id_question": 4,
            "question_text": "Would you rather have a job with more responsibilities but higher pay?",
            "question_type": "si/no"
        },
        {
            "id_question": 5,
            "question_text": "Which one do you prefer for data analysis?",
            "options": ["Python", "R", "Excel", "SQL"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 6,
            "question_text": "Which one is your favorite sport?",
            "options": ["Football", "Basketball", "Tennis", "Swimming"],
            "question_type": "eleccion simple"
        },{
            "id_question": 7,
            "question_text": "Do you like working in a team?",
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "question_text": "How many hours do you sleep per day?",
            "question_type": "numericas"
        }
    ]
},{"id_survey": 4,
    "creator": 'creador',
    "name": "Testing survey4",
    "description": "This is just testing survey",
    "published": true,
    "questions": [
        {
            "id_question": 1,
            "question_text": 'why did the chicken crossed the road?',
            "question_type": 'calificacion'
        },{
            "id_question": 2,
            "question_text": 'is red a color?',
            "question_type": 'si/no'
        },{
            "id_question": 3,
            "question_text": "Do you prefer coffee or tea?",
            "options": ["Coffee", "Tea"],
            "question_type": 'eleccion simple'
        },
        {
            "id_question": 4,
            "question_text": "Which one is your favorite beverage?",
            "options": ["Coffee", "Tea", "Juice", "Water"],
            "question_type": "eleccion simple"
        },
        {
            "id_question": 5,
            "question_text": "Is Java a statically typed language?",
            "question_type": "si/no"
        },
        {
            "id_question": 6,
            "question_text": "How many hours do you work per day?",
            "question_type": "numericas"
        },
        {
            "id_question": 7,
            "question_text": "Would you rather work from home or in an office?",
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "question_text": "Which one do you prefer for mobile app development?",
            "options": ["React Native", "Flutter", "Swift", "Kotlin"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 9,
            "question_text": "How much would you rate your mobile app development skills?",
            "question_type": "calificacion"
        },
        {
            "id_question": 10,
            "question_text": "Do you like working on weekends?",
            "question_type": "si/no"
        },
        {
            "id_question": 11,
            "question_text": "Which one is your favorite mobile operating system?",
            "options": ["Android", "iOS", "Windows Phone", "BlackBerry"],
            "question_type": "eleccion simple"
        },
        {
            "id_question": 12,
            "question_text": "How much would you rate your problem-solving skills?",
            "question_type": "calificacion"
        }
    ]
}])


// Datos de preuba 
// Se generan las respuestas
dbSurveys.createCollection('answers');
dbSurveys['answers'].insertMany([
    {"id_survey": 4,
    "id_respondent": 1,
    "answers": [
            {
                "id_question": 1,
                "answer": 85,
                "question_type": "calificacion"
            },
            {
                "id_question": 2,
                "answer": 1,
                "question_type": "si/no"
            },
            {
                "id_question": 3,
                "answer": "Coffee",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 4,
                "answer": "Juice",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 5,
                "answer": 1,
                "question_type": "si/no"
            },
            {
                "id_question": 6,
                "answer": 8,
                "question_type": "numericas"
            },
            {
                "id_question": 7,
                "answer": 0,
                "question_type": "si/no"
            },
            {
                "id_question": 8,
                "answer": ["React Native", "Swift"],
                "question_type": "eleccion multiple"
            },
            {
                "id_question": 9,
                "answer": 75,
                "question_type": "calificacion"
            },
            {
                "id_question": 10,
                "answer": 0,
                "question_type": "si/no"
            },
            {
                "id_question": 11,
                "answer": "Android",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 12,
                "answer": 90,
                "question_type": "calificacion"
            }
        ]
    },{"id_survey": 4,
    "id_respondent": 2,
    "answers": [
        {
                "id_question": 1,
                "answer": 95,
                "question_type": "calificacion"
            },
            {
                "id_question": 2,
                "answer": 0,
                "question_type": "si/no"
            },
            {
                "id_question": 3,
                "answer": "Tea",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 4,
                "answer": "Water",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 5,
                "answer": 0,
                "question_type": "si/no"
            },
            {
                "id_question": 6,
                "answer": 7,
                "question_type": "numericas"
            },
            {
                "id_question": 7,
                "answer": 1,
                "question_type": "si/no"
            },
            {
                "id_question": 8,
                "answer": ["Flutter", "Kotlin"],
                "question_type": "eleccion multiple"
            },
            {
                "id_question": 9,
                "answer": 80,
                "question_type": "calificacion"
            },
            {
                "id_question": 10,
                "answer": 1,
                "question_type": "si/no"
            },
            {
                "id_question": 11,
                "answer": "iOS",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 12,
                "answer": 85,
                "question_type": "calificacion"
            }
        ]
    },{"id_survey": 4,
    "id_respondent": 3,
    "answers": [
            {
                "id_question": 1,
                "answer": 70,
                "question_type": "calificacion"
            },
            {
                "id_question": 2,
                "answer": 0,
                "question_type": "si/no"
            },
            {
                "id_question": 3,
                "answer": "Coffee",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 4,
                "answer": "Coffee",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 5,
                "answer": 1,
                "question_type": "si/no"
            },
            {
                "id_question": 6,
                "answer": 10,
                "question_type": "numericas"
            },
            {
                "id_question": 7,
                "answer": 0,
                "question_type": "si/no"
            },
            {
                "id_question": 8,
                "answer": ["Flutter", "React Native", "Kotlin"],
                "question_type": "eleccion multiple"
            },
            {
                "id_question": 9,
                "answer": 65,
                "question_type": "calificacion"
            },
            {
                "id_question": 10,
                "answer": 1,
                "question_type": "si/no"
            },
            {
                "id_question": 11,
                "answer": "Android",
                "question_type": "eleccion simple"
            },
            {
                "id_question": 12,
                "answer": 75,
                "question_type": "calificacion"
            }
        ]
    },{"id_survey": 4,
    "id_respondent": 4,
    "answers": [
        {
            "id_question": 1,
            "answer": 60,
            "question_type": "calificacion"
        },
        {
            "id_question": 2,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "Tea",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": "Water",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 5,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 6,
            "answer": 6,
            "question_type": "numericas"
        },
        {
            "id_question": 7,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": ["React Native"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 9,
            "answer": 70,
            "question_type": "calificacion"
        },
        {
            "id_question": 10,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 11,
            "answer": "Windows Phone",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 12,
            "answer": 80,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 1,
    "id_respondent": 5,
    "answers": [
        {
            "id_question": 1,
            "answer": "Because he found meaning in his endless task.",
            "question_type": "abierta"
        },
        {
            "id_question": 2,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "Computer science",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": "Because it provides a lightweight way to virtualize applications and their environments.",
            "question_type": "abierta"
        },
        {
            "id_question": 5,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 6,
            "answer": 15,
            "question_type": "numericas"
        },
        {
            "id_question": 7,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": ["The beach", "The mountain"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 9,
            "answer": 50,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 1,
    "id_respondent": 6,
    "answers": [
        {
            "id_question": 1,
            "answer": "Because he found contentment in his eternal task.",
            "question_type": "abierta"
        },
        {
            "id_question": 2,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "Systems engineering",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": "Because it provides a consistent and reproducible environment for applications.",
            "question_type": "abierta"
        },
        {
            "id_question": 5,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 6,
            "answer": 7,
            "question_type": "numericas"
        },
        {
            "id_question": 7,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": ["The beach", "River"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 9,
            "answer": 90,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 1,
    "id_respondent": 7,
    "answers": [
        {
            "id_question": 1,
            "answer": "Because he embraced his fate and found purpose in his task.",
            "question_type": "abierta"
        },
        {
            "id_question": 2,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "Computer engineering",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": "Because it allows for containerization, making applications more portable and environments more controlled.",
            "question_type": "abierta"
        },
        {
            "id_question": 5,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 6,
            "answer": 8,
            "question_type": "numericas"
        },
        {
            "id_question": 7,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": ["None"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 9,
            "answer": 95,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 1,
    "id_respondent": 1,
    "answers": [
        {
            "id_question": 1,
            "answer": "Because he found contentment in his eternal task.",
            "question_type": "abierta"
        },
        {
            "id_question": 2,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "Computer engineering",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": "Because it provides a consistent and reproducible environment for applications.",
            "question_type": "abierta"
        },
        {
            "id_question": 5,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 6,
            "answer": 8,
            "question_type": "numericas"
        },
        {
            "id_question": 7,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": ["The beach"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 9,
            "answer": 60,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 2,
    "id_respondent": 2,
    "answers": [
        {
            "id_question": 1,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 2,
            "answer": "Python",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 3,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 4,
            "answer": 5,
            "question_type": "numericas"
        },
        {
            "id_question": 5,
            "answer": "back-end",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 6,
            "answer": 85,
            "question_type": "calificacion"
        },
        {
            "id_question": 7,
            "answer": "Visual Studio Code",
            "question_type": "abierta"
        },
        {
            "id_question": 8,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 9,
            "answer": "Dog",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 10,
            "answer": 80,
            "question_type": "calificacion"
        },
        {
            "id_question": 11,
            "answer": 50,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 2,
    "id_respondent": 5,
    "answers": [
        {
            "id_question": 1,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 2,
            "answer": "Java",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 3,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 4,
            "answer": 3,
            "question_type": "numericas"
        },
        {
            "id_question": 5,
            "answer": "front-end",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 6,
            "answer": 75,
            "question_type": "calificacion"
        },
        {
            "id_question": 7,
            "answer": "PyCharm",
            "question_type": "abierta"
        },
        {
            "id_question": 8,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 9,
            "answer": "Cat",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 10,
            "answer": 70,
            "question_type": "calificacion"
        },
        {
            "id_question": 11,
            "answer": 80,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 2,
    "id_respondent": 9,
    "answers": [
        {
            "id_question": 1,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 2,
            "answer": "C++",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 3,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 4,
            "answer": 4,
            "question_type": "numericas"
        },
        {
            "id_question": 5,
            "answer": "front-end",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 6,
            "answer": 70,
            "question_type": "calificacion"
        },
        {
            "id_question": 7,
            "answer": "IntelliJ IDEA",
            "question_type": "abierta"
        },
        {
            "id_question": 8,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 9,
            "answer": "Fish",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 10,
            "answer": 60,
            "question_type": "calificacion"
        },
        {
            "id_question": 11,
            "answer": 60,
            "question_type": "calificacion"
        }
    ]
    
    },{"id_survey": 3,
    "id_respondent": 7,
    "answers": [
        {
            "id_question": 1,
            "answer": 5,
            "question_type": "numericas"
        },
        {
            "id_question": 2,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "Yes",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 5,
            "answer": ["Python", "R"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 6,
            "answer": "Football",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 7,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": 7,
            "question_type": "numericas"
        }
    ]
    
    },{"id_survey": 3,
    "id_respondent": 4,
    "answers": [
        {
            "id_question": 1,
            "answer": 11,
            "question_type": "numericas"
        },
        {
            "id_question": 2,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "Maybe",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 5,
            "answer": ["Python", "Excel"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 6,
            "answer": "Tennis",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 7,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": 6,
            "question_type": "numericas"
        }
    ]
    
    },{"id_survey": 3,
    "id_respondent": 3,
    "answers": [
        {
            "id_question": 1,
            "answer": 4,
            "question_type": "numericas"
        },
        {
            "id_question": 2,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 3,
            "answer": "I don't know",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 4,
            "answer": 1,
            "question_type": "si/no"
        },
        {
            "id_question": 5,
            "answer": ["R", "SQL"],
            "question_type": "eleccion multiple"
        },
        {
            "id_question": 6,
            "answer": "Swimming",
            "question_type": "eleccion simple"
        },
        {
            "id_question": 7,
            "answer": 0,
            "question_type": "si/no"
        },
        {
            "id_question": 8,
            "answer": 8,
            "question_type": "numericas"
        }
    ]
    
    },
    ]);