def kyc_passed(kyc_status) -> bool:
    if not kyc_status:
        return False

    if "review_status" in kyc_status:
        return kyc_status["review_status"].upper() == "APPROVED"

    return (
            "review_result" in kyc_status and kyc_status["review_result"].upper() == "GREEN"
    )


def kyc_rejected(kyc_status) -> bool:
    if not kyc_status:
        return False

    if "review_status" in kyc_status:
        return kyc_status["review_status"].upper() == "REJECTED"

    return (
            "review_result" in kyc_status and kyc_status["review_result"].upper() == "RED"
    )