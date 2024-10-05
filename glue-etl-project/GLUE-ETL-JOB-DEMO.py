import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','S3_INPUT_PATH','S3_OUTPUT_PATH','COL_TO_DROP'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
S3_INPUT_PATH=args['S3_INPUT_PATH']
S3_OUTPUT_PATH=args['S3_OUTPUT_PATH']
COL_TO_DROP=args['COL_TO_DROP']

#read data from S3
df=spark.read.option('header','true').csv(S3_INPUT_PATH)

#drop column
df=df.drop(COL_TO_DROP)

#write data to s3 bucket
df=df.repartition(1).write.mode("overwrite").parquet(S3_OUTPUT_PATH)

job.commit()

#Parameters passed in advance settings :

#--S3_INPUT_PATH : s3://pyspark-project-bucket/input/hotel_bookings 2.csv
#--S3_OUTPUT_PATH : s3://pyspark-project-bucket/output/
#--COL_TO_DROP : arrival_date_month