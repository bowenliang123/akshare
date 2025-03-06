from collections.abc import Generator
from typing import Any

import akshare as ak
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class StockBidAskEmTool(Tool):
    """
    stock_bid_ask_em
    东方财富-行情报价
    https://akshare.akfamily.xyz/data/stock/stock.html#id9
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        param_symbol: str = tool_parameters.get("symbol", "000776")
        if not param_symbol:
            raise ValueError("股票代码symbol is required.")

        print(param_symbol)
        print("param_symbol")

        # query
        df = ak.stock_bid_ask_em(symbol=param_symbol)

        # filter
        filtered_items = ["最新", "最高", "最低"]
        filtered_df = df[df['item'].isin(filtered_items)]

        # format
        filtered_df['_result'] = filtered_df['item'] + ':' + filtered_df['value'].apply(str)
        details = filtered_df['_result'].to_string(index=False).replace("\n", "，")

        # assemble
        result_str = f"股票代码{param_symbol}的行情报价，{details}。"

        yield self.create_text_message("happy")
