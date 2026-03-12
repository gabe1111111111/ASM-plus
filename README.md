# Java Project

A basic Maven-based Java project scaffold.

## Project Structure

```
.
├── src/
│   ├── main/java/com/example/
│   │   └── App.java
│   └── test/java/com/example/
│       └── AppTest.java
├── pom.xml
└── README.md
```

## Building

Build the project with Maven:

```bash
mvn clean package
```

## Running

Run the application:

```bash
mvn exec:java -Dexec.mainClass="com.example.App"
```

Or execute the JAR file:

```bash
java -jar target/java-project-1.0-SNAPSHOT.jar
```

## Testing

Run tests:

```bash
mvn test
```

## Requirements

- Java 11 or higher
- Maven 3.6.0 or higher
