## 2026.01.07 16:07:04

### RU
- развернул Apache Spark локально через Docker
- запустил PySpark и Spark UI
- понял модель выполнения: партиции → tasks → stages → jobs
- сгенерировал большой датасет через `spark.range`
- записал данные в файловую систему Spark-способом (много `part-*`)
- осознанно применил антипаттерн `coalesce(1)` и получил один файл ~1.4 ГБ
- на практике увидел разницу между параллельной и однопоточной обработкой
- убедился, что Spark стабильно работает с объёмами, где Python концептуально упирается
- зафиксировал понимание: Spark — это не БД и не библиотека, а движок распределённых вычислений

### EN
- deployed Apache Spark locally using Docker
- started PySpark and explored Spark UI
- understood the execution model: partitions → tasks → stages → jobs
- generated a large dataset using `spark.range`
- wrote data in a Spark-native way (multiple `part-*` files)
- intentionally applied the `coalesce(1)` antipattern to produce a single ~1.4 GB file
- clearly observed the difference between parallel and single-threaded processing
- confirmed that Spark handles data volumes where plain Python becomes impractical
- solidified the idea that Spark is a distributed computation engine, not a database or a simple library


## 2026.01.07 15:14:04 

- скачал курс по Spark с торрентов  
- нашёл релевантные каналы и видео на YouTube  
- посмотрел первые лекции  
- в общих чертах понял, что такое Spark и как он используется  
- решил перейти к первому практическому примеру (hello world)
