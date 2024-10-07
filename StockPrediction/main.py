import asyncio
import logging
import time
from src.data_processing import DataProcessor
from src.data_fetch import async_fetch_data, combine_file
from src.models import ProphetModel
import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

async def main():
    await async_fetch_data()
    print("Sleeping ... %.2fs" % 3)
    time.sleep(3)
    logFormatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s:%(message)s")
    logger = logging.getLogger(__name__)

    
    logger.info("BẮT ĐẦU ĐỌC FILE VÀ XỬ LÝ DỮ LIỆU======>")

    combine_file('/Users/hieppx/Documents/Workspace/MICE3/StockPrediction/datasets/HOSE_datasets')
    df = pd.read_csv('/Users/hieppx/Documents/Workspace/MICE3/StockPrediction/datasets/lastest_combined_file.csv', parse_dates=['time'])

    dataprocessor = DataProcessor(prediction_length=28)
    training_df, _, _ = dataprocessor._get_cv_split(df, split_num = 0, validation=True)
    logger.info("Prediction: data for prediction obtained")

    pred_date = (dataprocessor.get_max_date() + timedelta(days = 1))

    # pass data to model
    model = ProphetModel()
    predictions_df = model.prophet_predictions(training_df, cv = 0, pred_date = pred_date)
    logger.info("Prediction: predictions made")

    predictions_df.to_csv('/Users/hieppx/Documents/Workspace/MICE3/StockPrediction/datasets/prediction_file.csv', index=False)

    dataprocessor.get_final_prediction(df, predictions_df)

# asyncio.run(main())
if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    # Lên lịch cho hàm main chạy vào lúc 17h20 hàng ngày
    scheduler.add_job(main, 'cron', hour=18, minute=0)
    # Bắt đầu scheduler
    scheduler.start()
    try:
        # Giữ chương trình chạy
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass