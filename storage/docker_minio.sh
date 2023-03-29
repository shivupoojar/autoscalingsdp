docker start 91e
docker exec -it 91e mc mb minio/aeneas
docker exec -it 91e mc mb minio/aeneas-output
docker exec -it 91e mc cp data/p001.xhtml minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_1.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_2.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_3.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_4.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_5.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_6.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_7.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_8.wav minio/aeneas
docker exec -it 91e mc cp data/documents/p001_out_9.wav minio/aeneas
