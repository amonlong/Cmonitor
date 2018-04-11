#-*- coding: utf-8 -*-

#客户经理月绩效
# 实际贷出金额(payMoney)
# 实际回收金额(repaidMoney,包含展期费等，数据从loan_repaid中来)
MONTHPERFORMANCE = """
	SELECT s1.lenderId
		,s1.month
		,IF (s1.sumPayMoney IS NULL,0,s1.sumPayMoney) AS sumPayMoney
		,IF (s2.sumPaidMoney IS NULL,0,s2.sumPaidMoney) AS sumPaidMoney
		,( IF (s2.sumPaidMoney IS NULL,0,s2.sumPaidMoney) - IF (s1.sumPayMoney IS NULL,0,s1.sumPayMoney) ) * 0.15 AS reward
		,CURDATE() AS createDate
	FROM (
		SELECT l.lenderId
			,DATE_FORMAT(lr.createdTime, '%Y-%m') AS month
			,sum(l.payMoney) AS sumPayMoney
		FROM loan l
			,loan_repaying lr
		WHERE l.id = lr.loanId
		AND l.STATUS = 6
		AND l.productId in ('')
		AND l.firmId in ('')
		GROUP BY
			l.lenderId, month
		) s1
	LEFT JOIN (
		SELECT l.lenderId
			,DATE_FORMAT(date_sub(lrd.repaidTime,INTERVAL 7 DAY),'%Y-%m') AS month,
			sum(lrd.repaidMoney) AS sumPaidMoney
		FROM loan l
			,loan_repaid lrd
		WHERE l.id = lrd.loanId
		AND l.STATUS = 6
		AND l.productId in ('')
		AND l.firmId in ('')
		AND lrd.STATUS = 3
		AND lrd.repaidTime IS NOT NULL
		AND DATEDIFF(lrd.repaidTime,lrd.termDate) <= 7
		GROUP BY 
			l.lenderId, month
	) s2 ON s1.lenderId = s2.lenderId
	AND s1.month = s2.month
"""