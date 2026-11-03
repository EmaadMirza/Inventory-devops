FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY target/mini-inventory.jar app.jar
USER 10001:10001
ENV APP_PORT=8080
EXPOSE 8080
ENTRYPOINT ["java","-Xms16m","-Xmx96m","-jar","/app/app.jar"]
