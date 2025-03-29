import requests
import json
from datetime import datetime, timedelta

def get_and_extract_hotels(city_id, checkin=None, checkout=None):
    if not checkin:
        checkin = datetime.now().strftime("%Y-%m-%d")
    if not checkout:
        checkout = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    url = "https://www.agoda.com/graphql/search"

    headers = {
        'Ag-Debug-Override-Origin': 'IN',
        'Ag-Language-Locale': 'en-us',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
    }

    payload = json.dumps({
        "operationName": "citySearch",
        "variables": {
            "CitySearchRequest": {
                "cityId": int(city_id),
                "searchRequest": {
                    "searchCriteria": {
                        "isAllowBookOnRequest": True,
                        "localCheckInDate": checkin,
                        "los": 1,
                        "rooms": 1,
                        "adults": 1,
                        "children": 0,
                        "childAges": [],
                        "ratePlans": [],
                        "featureFlagRequest": {
                            "fetchNamesForTealium": True,
                            "fiveStarDealOfTheDay": True,
                            "isAllowBookOnRequest": False,
                            "showUnAvailable": True,
                            "showRemainingProperties": True,
                            "isMultiHotelSearch": False,
                            "enableAgencySupplyForPackages": True,
                            "enablePageToken": True,
                            "enableDealsOfTheDayFilter": False,
                            "isEnableSupplierFinancialInfo": False,
                            "ignoreRequestedNumberOfRoomsForNha": False
                        },
                        "isUserLoggedIn": True,
                        "currency": "INR",
                        "travellerType": "Couple",
                        "sorting": {
                            "sortField": "Ranking",
                            "sortOrder": "Desc",
                            "sortParams": None
                        },
                        "requiredBasis": "PRPN",
                        "requiredPrice": "Exclusive",
                        "suggestionLimit": 0,
                        "synchronous": False,
                        "supplierPullMetadataRequest": None,
                        "isRoomSuggestionRequested": False,
                        "isAPORequest": False,
                        "hasAPOFilter": False
                    },
                    "searchContext": {
                        "memberId": 412653356,
                        "locale": "en-in",
                        "cid": 1844104,
                        "origin": "IN",
                        "platform": 1,
                        "endpointSearchType": "CitySearch"
                    },
                    "matrixGroup": [
                        {
                            "matrixGroup": "NumberOfBedrooms",
                            "size": 100
                        },
                        {
                            "matrixGroup": "LandmarkIds",
                            "size": 10
                        },
                        {
                            "matrixGroup": "GroupedBedTypes",
                            "size": 100
                        },
                        {
                            "matrixGroup": "RoomBenefits",
                            "size": 100
                        },
                        {
                            "matrixGroup": "AtmosphereIds",
                            "size": 100
                        },
                        {
                            "matrixGroup": "PopularForFamily",
                            "size": 5
                        },
                        {
                            "matrixGroup": "RoomAmenities",
                            "size": 100
                        },
                        {
                            "matrixGroup": "AffordableCategory",
                            "size": 100
                        },
                        {
                            "matrixGroup": "HotelFacilities",
                            "size": 100
                        },
                        {
                            "matrixGroup": "BeachAccessTypeIds",
                            "size": 100
                        },
                        {
                            "matrixGroup": "StarRating",
                            "size": 20
                        },
                        {
                            "matrixGroup": "KidsStayForFree",
                            "size": 5
                        },
                        {
                            "matrixGroup": "AllGuestReviewBreakdown",
                            "size": 100
                        },
                        {
                            "matrixGroup": "MetroSubwayStationLandmarkIds",
                            "size": 20
                        },
                        {
                            "matrixGroup": "CityCenterDistance",
                            "size": 100
                        },
                        {
                            "matrixGroup": "ProductType",
                            "size": 100
                        },
                        {
                            "matrixGroup": "TripPurpose",
                            "size": 5
                        },
                        {
                            "matrixGroup": "BusStationLandmarkIds",
                            "size": 20
                        },
                        {
                            "matrixGroup": "IsSustainableTravel",
                            "size": 2
                        },
                        {
                            "matrixGroup": "ReviewLocationScore",
                            "size": 3
                        },
                        {
                            "matrixGroup": "LandmarkSubTypeCategoryIds",
                            "size": 20
                        },
                        {
                            "matrixGroup": "ReviewScore",
                            "size": 100
                        },
                        {
                            "matrixGroup": "AccommodationType",
                            "size": 100
                        },
                        {
                            "matrixGroup": "PaymentOptions",
                            "size": 100
                        },
                        {
                            "matrixGroup": "TrainStationLandmarkIds",
                            "size": 20
                        },
                        {
                            "matrixGroup": "HotelAreaId",
                            "size": 100
                        },
                        {
                            "matrixGroup": "HotelChainId",
                            "size": 10
                        },
                        {
                            "matrixGroup": "RecommendedByDestinationCity",
                            "size": 10
                        },
                        {
                            "matrixGroup": "Deals",
                            "size": 100
                        }
                    ],
                    "page": {
                        "pageSize": 100,
                        "pageNumber": 1,
                        "pageToken": ""
                    },
                    "searchDetailRequest": {
                        "priceHistogramBins": 50
                    },
                    "rankingRequest": {
                        "isNhaKeywordSearch": False
                    },
                    "rocketmilesRequestV2": None,
                    "featuredPulsePropertiesRequest": {
                        "numberOfPulseProperties": 15
                    }
                }
            },
            "ContentSummaryRequest": {
                "context": {
                    "userOrigin": "IN",
                    "locale": "en-in",
                    "forceExperimentsByIdNew": [
                        {
                            "key": "UMRAH-B2B",
                            "value": "B"
                        },
                        {
                            "key": "UMRAH-B2C-REGIONAL",
                            "value": "B"
                        },
                        {
                            "key": "UMRAH-B2C",
                            "value": "Z"
                        },
                        {
                            "key": "JGCW-204",
                            "value": "B"
                        }
                    ],
                    "apo": False,
                    "searchCriteria": {
                        "cityId": int(city_id)
                    },
                    "platform": {
                        "id": 1
                    },
                    "storeFrontId": 3,
                    "cid": "1844104",
                    "occupancy": {
                        "numberOfAdults": 1,
                        "numberOfChildren": 0,
                        "travelerType": 0,
                        "checkIn": checkin + "T17:00:00.000Z"
                    },
                    "deviceTypeId": 1,
                    "whiteLabelKey": "",
                    "correlationId": ""
                },
                "summary": {
                    "highlightedFeaturesOrderPriority": None,
                    "includeHotelCharacter": True
                },
                "reviews": {
                    "commentary": None,
                    "demographics": {
                        "providerIds": None,
                        "filter": {
                            "defaultProviderOnly": True
                        }
                    },
                    "summaries": {
                        "providerIds": None,
                        "apo": True,
                        "limit": 1,
                        "travellerType": 0
                    },
                    "cumulative": {
                        "providerIds": None
                    },
                    "filters": None
                },
                "images": {
                    "page": None,
                    "maxWidth": 0,
                    "maxHeight": 0,
                    "imageSizes": None,
                    "indexOffset": None
                },
                "rooms": {
                    "images": None,
                    "featureLimit": 0,
                    "filterCriteria": None,
                    "includeMissing": False,
                    "includeSoldOut": False,
                    "includeDmcRoomId": False,
                    "soldOutRoomCriteria": None,
                    "showRoomSize": True,
                    "showRoomFacilities": True,
                    "showRoomName": False
                },
                "nonHotelAccommodation": True,
                "engagement": True,
                "highlights": {
                    "maxNumberOfItems": 0,
                    "images": {
                        "imageSizes": [
                            {
                                "key": "full",
                                "size": {
                                    "width": 0,
                                    "height": 0
                                }
                            }
                        ]
                    }
                },
                "personalizedInformation": True,
                "localInformation": {
                    "images": None
                },
                "features": None,
                "rateCategories": True,
                "contentRateCategories": {
                    "escapeRateCategories": {}
                },
                "synopsis": True
            },
            "PricingSummaryRequest": {
                "cheapestOnly": True,
                "context": {
                    "isAllowBookOnRequest": True,
                    "abTests": [
                        {
                            "testId": 9021,
                            "abUser": "B"
                        },
                        {
                            "testId": 9023,
                            "abUser": "B"
                        },
                        {
                            "testId": 9024,
                            "abUser": "B"
                        },
                        {
                            "testId": 9025,
                            "abUser": "B"
                        },
                        {
                            "testId": 9027,
                            "abUser": "B"
                        },
                        {
                            "testId": 9029,
                            "abUser": "B"
                        }
                    ],
                    "clientInfo": {
                        "cid": 1844104,
                        "languageId": 1,
                        "languageUse": 1,
                        "origin": "IN",
                        "platform": 1,
                        "searchId": "2af9e43a-d91a-42d6-a5b3-482e516e96c4",
                        "storefront": 3,
                        "userId": "b89971a3-cb99-4a68-ba48-578deb797770"
                    },
                    "experiment": [
                        {
                            "name": "UMRAH-B2B",
                            "variant": "B"
                        },
                        {
                            "name": "UMRAH-B2C-REGIONAL",
                            "variant": "B"
                        },
                        {
                            "name": "UMRAH-B2C",
                            "variant": "Z"
                        },
                        {
                            "name": "JGCW-204",
                            "variant": "B"
                        }
                    ],
                    "sessionInfo": {
                        "isLogin": True,
                        "memberId": 412653356,
                        "sessionId": 1
                    },
                    "packaging": None
                },
                "isSSR": True,
                "pricing": {
                    "bookingDate": checkin+ "T16:35:41.060Z",
                    "checkIn": checkin + "T17:00:00.000Z",
                    "checkout": checkout + "T17:00:00.000Z",
                    "localCheckInDate": checkin,
                    "localCheckoutDate": (datetime.strptime(checkout, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),

                    "currency": "INR",
                    "details": {
                        "cheapestPriceOnly": False,
                        "itemBreakdown": False,
                        "priceBreakdown": False
                    },
                    "features": {
                        "crossOutRate": False,
                        "isAPSPeek": False,
                        "isAllOcc": False,
                        "isApsEnabled": False,
                        "isIncludeUsdAndLocalCurrency": False,
                        "isMSE": True,
                        "isRPM2Included": True,
                        "maxSuggestions": 0,
                        "isEnableSupplierFinancialInfo": False,
                        "isLoggingAuctionData": False,
                        "newRateModel": False,
                        "overrideOccupancy": False,
                        "filterCheapestRoomEscapesPackage": False,
                        "priusId": 0,
                        "synchronous": False,
                        "enableRichContentOffer": True,
                        "showCouponAmountInUserCurrency": False,
                        "disableEscapesPackage": False,
                        "enablePushDayUseRates": False,
                        "enableDayUseCor": False
                    },
                    "filters": {
                        "cheapestRoomFilters": [],
                        "filterAPO": False,
                        "ratePlans": [
                            1
                        ],
                        "secretDealOnly": False,
                        "suppliers": [],
                        "nosOfBedrooms": []
                    },
                    "includedPriceInfo": False,
                    "occupancy": {
                        "adults": 1,
                        "children": 0,
                        "childAges": [],
                        "rooms": 1,
                        "childrenTypes": []
                    },
                    "supplierPullMetadata": {
                        "requiredPrecheckAccuracyLevel": 0
                    },
                    "mseHotelIds": [],
                    "ppLandingHotelIds": [],
                    "searchedHotelIds": [],
                    "paymentId": -1,
                    "externalLoyaltyRequest": None
                },
                "suggestedPrice": "Exclusive"
            },
            "PriceStreamMetaLabRequest": {
                "attributesId": [
                    8,
                    1,
                    18,
                    7,
                    11,
                    2,
                    3
                ]
            }
        },
        "query": "query citySearch($CitySearchRequest: CitySearchRequest!, $ContentSummaryRequest: ContentSummaryRequest!, $PricingSummaryRequest: PricingRequestParameters, $PriceStreamMetaLabRequest: PriceStreamMetaLabRequest) {\n  citySearch(CitySearchRequest: $CitySearchRequest) {\n    featuredPulseProperties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest) {\n      propertyId\n      propertyResultType\n      pricing {\n        pulseCampaignMetadata {\n          promotionTypeId\n          webCampaignId\n          campaignTypeId\n          campaignBadgeText\n          campaignBadgeDescText\n          dealExpiryTime\n          showPulseMerchandise\n        }\n        isAvailable\n        isReady\n        offers {\n          roomOffers {\n            room {\n              pricing {\n                currency\n                price {\n                  perNight {\n                    exclusive {\n                      crossedOutPrice\n                      display\n                    }\n                    inclusive {\n                      crossedOutPrice\n                      display\n                    }\n                  }\n                  perRoomPerNight {\n                    exclusive {\n                      crossedOutPrice\n                      display\n                    }\n                    inclusive {\n                      crossedOutPrice\n                      display\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n      content {\n        reviews {\n          contentReview {\n            isDefault\n            providerId\n            cumulative {\n              reviewCount\n              score\n            }\n          }\n          cumulative {\n            reviewCount\n            score\n          }\n        }\n        images {\n          hotelImages {\n            urls {\n              value\n            }\n          }\n        }\n        informationSummary {\n          hasHostExperience\n          displayName\n          rating\n          propertyLinks {\n            propertyPage\n          }\n          address {\n            country {\n              id\n            }\n            area {\n              name\n            }\n            city {\n              name\n            }\n          }\n          nhaSummary {\n            hostType\n          }\n        }\n      }\n    }\n    searchResult {\n      sortMatrix {\n        result {\n          fieldId\n          sorting {\n            sortField\n            sortOrder\n            sortParams {\n              id\n            }\n          }\n          display {\n            name\n          }\n          childMatrix {\n            fieldId\n            sorting {\n              sortField\n              sortOrder\n              sortParams {\n                id\n              }\n            }\n            display {\n              name\n            }\n            childMatrix {\n              fieldId\n              sorting {\n                sortField\n                sortOrder\n                sortParams {\n                  id\n                }\n              }\n              display {\n                name\n              }\n            }\n          }\n        }\n      }\n      searchInfo {\n        flexibleSearch {\n          currentDate {\n            checkIn\n            price\n          }\n          alternativeDates {\n            checkIn\n            price\n          }\n        }\n        hasSecretDeal\n        isComplete\n        totalFilteredHotels\n        hasEscapesPackage\n        searchStatus {\n          searchCriteria {\n            checkIn\n          }\n          searchStatus\n        }\n        objectInfo {\n          objectName\n          cityName\n          cityEnglishName\n          countryId\n          countryEnglishName\n          mapLatitude\n          mapLongitude\n          mapZoomLevel\n          wlPreferredCityName\n          wlPreferredCountryName\n          cityId\n          cityCenterPolygon {\n            geoPoints {\n              lon\n              lat\n            }\n            touristAreaCenterPoint {\n              lon\n              lat\n            }\n          }\n        }\n      }\n      urgencyDetail {\n        urgencyScore\n      }\n      histogram {\n        bins {\n          numOfElements\n          upperBound {\n            perNightPerRoom\n            perPax\n          }\n        }\n      }\n      nhaProbability\n    }\n    properties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest, PriceStreamMetaLabRequest: $PriceStreamMetaLabRequest) {\n      propertyId\n      sponsoredDetail {\n        sponsoredType\n        trackingData\n        isShowSponsoredFlag\n      }\n      propertyResultType\n      content {\n        informationSummary {\n          hotelCharacter {\n            hotelTag {\n              name\n              symbol\n            }\n            hotelView {\n              name\n              symbol\n            }\n          }\n          propertyLinks {\n            propertyPage\n          }\n          atmospheres {\n            id\n            name\n          }\n          isSustainableTravel\n          localeName\n          defaultName\n          displayName\n          accommodationType\n          awardYear\n          hasHostExperience\n          nhaSummary {\n            hostPropertyCount\n          }\n          address {\n            countryCode\n            country {\n              id\n              name\n            }\n            city {\n              id\n              name\n            }\n            area {\n              id\n              name\n            }\n          }\n          propertyType\n          rating\n          agodaGuaranteeProgram\n          remarks {\n            renovationInfo {\n              renovationType\n              year\n            }\n          }\n          spokenLanguages {\n            id\n          }\n          geoInfo {\n            latitude\n            longitude\n          }\n        }\n        propertyEngagement {\n          lastBooking\n          peopleLooking\n        }\n        nonHotelAccommodation {\n          masterRooms {\n            noOfBathrooms\n            noOfBedrooms\n            noOfBeds\n            roomSizeSqm\n            highlightedFacilities\n          }\n          hostLevel {\n            id\n            name\n          }\n          supportedLongStay\n        }\n        facilities {\n          id\n        }\n        images {\n          hotelImages {\n            id\n            caption\n            providerId\n            urls {\n              key\n              value\n            }\n          }\n        }\n        reviews {\n          contentReview {\n            isDefault\n            providerId\n            demographics {\n              groups {\n                id\n                grades {\n                  id\n                  score\n                }\n              }\n            }\n            summaries {\n              recommendationScores {\n                recommendationScore\n              }\n              snippets {\n                countryId\n                countryCode\n                countryName\n                date\n                demographicId\n                demographicName\n                reviewer\n                reviewRating\n                snippet\n              }\n            }\n            cumulative {\n              reviewCount\n              score\n            }\n          }\n          cumulative {\n            reviewCount\n            score\n          }\n          cumulativeForHost {\n            hostAvgHotelReviewRating\n            hostHotelReviewTotalCount\n          }\n        }\n        familyFeatures {\n          hasChildrenFreePolicy\n          isFamilyRoom\n          hasMoreThanOneBedroom\n          isInterConnectingRoom\n          isInfantCottageAvailable\n          hasKidsPool\n          hasKidsClub\n        }\n        personalizedInformation {\n          childrenFreePolicy {\n            fromAge\n            toAge\n          }\n        }\n        localInformation {\n          landmarks {\n            transportation {\n              landmarkName\n              distanceInM\n            }\n            topLandmark {\n              landmarkName\n              distanceInM\n            }\n            beach {\n              landmarkName\n              distanceInM\n            }\n          }\n          hasAirportTransfer\n        }\n        highlight {\n          cityCenter {\n            distanceFromCityCenter\n          }\n          favoriteFeatures {\n            features {\n              id\n              title\n              category\n            }\n          }\n          hasNearbyPublicTransportation\n        }\n        rateCategories {\n          escapeRateCategories {\n            rateCategoryId\n            localizedRateCategoryName\n          }\n        }\n      }\n      soldOut {\n        soldOutPrice {\n          averagePrice\n        }\n      }\n      pricing {\n        pulseCampaignMetadata {\n          promotionTypeId\n          webCampaignId\n          campaignTypeId\n          campaignBadgeText\n          campaignBadgeDescText\n          dealExpiryTime\n          showPulseMerchandise\n        }\n        isAvailable\n        isReady\n        benefits\n        cheapestRoomOffer {\n          agodaCash {\n            showBadge\n            giftcardGuid\n            dayToEarn\n            earnId\n            percentage\n            expiryDay\n          }\n          cashback {\n            cashbackGuid\n            showPostCashbackPrice\n            cashbackVersion\n            percentage\n            earnId\n            dayToEarn\n            expiryDay\n            cashbackType\n            appliedCampaignName\n          }\n        }\n        isEasyCancel\n        isInsiderDeal\n        suggestPriceType {\n          suggestPrice\n        }\n        roomBundle {\n          bundleId\n          bundleType\n          saveAmount {\n            perNight {\n              ...Frag6d65dh9e3168adh953ii\n            }\n          }\n        }\n        pointmax {\n          channelId\n          point\n        }\n        priceChange {\n          changePercentage\n          searchDate\n        }\n        payment {\n          cancellation {\n            cancellationType\n            freeCancellationDate\n          }\n          payLater {\n            isEligible\n          }\n          payAtHotel {\n            isEligible\n          }\n          noCreditCard {\n            isEligible\n          }\n          taxReceipt {\n            isEligible\n          }\n        }\n        cheapestStayPackageRatePlans {\n          stayPackageType\n          ratePlanId\n        }\n        pricingMessages {\n          location\n          ids\n        }\n        suppliersSummaries {\n          id\n          supplierHotelId\n        }\n        supplierInfo {\n          id\n          name\n          isAgodaBand\n        }\n        childPolicy {\n          freeChildren\n        }\n        offers {\n          roomOffers {\n            room {\n              extraPriceInfo {\n                displayPriceWithSurchargesPRPN\n                corDisplayPriceWithSurchargesPRPN\n              }\n              availableRooms\n              isPromoEligible\n              promotions {\n                typeId\n                promotionDiscount {\n                  value\n                }\n                isRatePlanAsPromotion\n                cmsTypeId\n                description\n              }\n              bookingDuration {\n                unit\n                value\n              }\n              supplierId\n              corSummary {\n                hasCor\n                corType\n                isOriginal\n                hasOwnCOR\n                isBlacklistedCor\n              }\n              localVoucher {\n                currencyCode\n                amount\n              }\n              pricing {\n                currency\n                price {\n                  perNight {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                  }\n                  perBook {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                  }\n                  perRoomPerNight {\n                    exclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                      loyaltyOfferSummary {\n                        basePrice {\n                          exclusive\n                          allInclusive\n                        }\n                        offers {\n                          identifier\n                          burn {\n                            points\n                            payableAmount\n                          }\n                          earn {\n                            points\n                          }\n                          offerType\n                          isSelected\n                        }\n                      }\n                    }\n                    inclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                      loyaltyOfferSummary {\n                        basePrice {\n                          exclusive\n                          allInclusive\n                        }\n                        offers {\n                          identifier\n                          burn {\n                            points\n                            payableAmount\n                          }\n                          earn {\n                            points\n                          }\n                          offerType\n                          isSelected\n                        }\n                      }\n                    }\n                  }\n                  totalDiscount\n                  priceAfterAppliedAgodaCash {\n                    perBook {\n                      ...Frag632gg60h4134523g2847\n                    }\n                    perRoomPerNight {\n                      ...Frag632gg60h4134523g2847\n                    }\n                  }\n                }\n                apsPeek {\n                  perRoomPerNight {\n                    ...Frag6d65dh9e3168adh953ii\n                  }\n                }\n                promotionPricePeek {\n                  display {\n                    perBook {\n                      ...Frag6d65dh9e3168adh953ii\n                    }\n                    perRoomPerNight {\n                      ...Frag6d65dh9e3168adh953ii\n                    }\n                    perNight {\n                      ...Frag6d65dh9e3168adh953ii\n                    }\n                  }\n                  discountType\n                  promotionCodeType\n                  promotionCode\n                  promoAppliedOnFinalPrice\n                  childPromotions {\n                    campaignId\n                  }\n                  campaignName\n                }\n                channelDiscountSummary {\n                  channelDiscountBreakdown {\n                    display\n                    discountPercent\n                    channelId\n                  }\n                }\n                packagePriceAndSaving {\n                  perPax {\n                    allInclusive {\n                      specialPriceAndSaving {\n                        baseChannel\n                        targetChannel\n                        targetPrice\n                        saving {\n                          amount\n                        }\n                      }\n                    }\n                  }\n                }\n                promotionsCumulative {\n                  promotionCumulativeType\n                  amountPercentage\n                  minNightsStay\n                }\n              }\n              uid\n              payment {\n                cancellation {\n                  cancellationType\n                }\n              }\n              discount {\n                deals\n                channelDiscount\n              }\n              saveUpTo {\n                perRoomPerNight\n              }\n              benefits {\n                id\n                targetType\n              }\n              channel {\n                id\n              }\n              mseRoomSummaries {\n                supplierId\n                subSupplierId\n                pricingSummaries {\n                  currency\n                  channelDiscountSummary {\n                    channelDiscountBreakdown {\n                      channelId\n                      discountPercent\n                      display\n                    }\n                  }\n                  price {\n                    perRoomPerNight {\n                      exclusive {\n                        display\n                      }\n                      inclusive {\n                        display\n                      }\n                    }\n                  }\n                }\n              }\n              cashback {\n                cashbackGuid\n                showPostCashbackPrice\n                cashbackVersion\n                percentage\n                earnId\n                dayToEarn\n                expiryDay\n                cashbackType\n                appliedCampaignName\n              }\n              agodaCash {\n                showBadge\n                giftcardGuid\n                dayToEarn\n                expiryDay\n                percentage\n              }\n              corInfo {\n                corBreakdown {\n                  taxExPN {\n                    ...Fragic8gi5326f4d5gb1c473\n                  }\n                  taxInPN {\n                    ...Fragic8gi5326f4d5gb1c473\n                  }\n                  taxExPRPN {\n                    ...Fragic8gi5326f4d5gb1c473\n                  }\n                  taxInPRPN {\n                    ...Fragic8gi5326f4d5gb1c473\n                  }\n                }\n                corInfo {\n                  corType\n                }\n              }\n              loyaltyDisplay {\n                items\n              }\n              capacity {\n                extraBedsAvailable\n              }\n              pricingMessages {\n                formatted {\n                  location\n                  texts {\n                    index\n                    text\n                  }\n                }\n              }\n              campaign {\n                selected {\n                  campaignId\n                  promotionId\n                  messages {\n                    campaignName\n                    title\n                    titleWithDiscount\n                    description\n                    linkOutText\n                    url\n                  }\n                }\n              }\n              isPackageEligible\n              stayPackageType\n            }\n          }\n        }\n      }\n      metaLab {\n        attributes {\n          attributeId\n          dataType\n          value\n          version\n        }\n      }\n      enrichment {\n        topSellingPoint {\n          tspType\n          value\n        }\n        pricingBadges {\n          badges\n        }\n        uniqueSellingPoint {\n          rank\n          segment\n          uspType\n          uspPropertyType\n        }\n        bookingHistory {\n          bookingCount {\n            count\n            timeFrame\n          }\n        }\n        showReviewSnippet\n        isPopular\n        roomInformation {\n          cheapestRoomSizeSqm\n          facilities {\n            id\n            propertyFacilityName\n            symbol\n          }\n        }\n      }\n    }\n    searchEnrichment {\n      suppliersInformation {\n        supplierId\n        supplierName\n        isAgodaBand\n      }\n      pageToken\n    }\n    aggregation {\n      matrixGroupResults {\n        matrixGroup\n        matrixItemResults {\n          id\n          name\n          count\n          filterKey\n          filterRequestType\n          extraDataResults {\n            text\n            matrixExtraDataType\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment Frag632gg60h4134523g2847 on DisplayPrice {\n  exclusive\n  allInclusive\n}\n\nfragment Frag6d65dh9e3168adh953ii on DFDisplayPrice {\n  exclusive\n  allInclusive\n}\n\nfragment Fragic8gi5326f4d5gb1c473 on DFCorBreakdownItem {\n  price\n  id\n}\n"
    })

    response = requests.post(url, headers=headers, data=payload)
    response_data = response.json()

    with open('search.json', 'w') as json_file:
        json.dump(response_data, json_file, indent=2)

    hotels_info = []

    if 'data' in response_data:
        properties = response_data['data']['citySearch']['properties']

        total_properties = response_data['data']['citySearch']['searchResult']['searchInfo']['totalFilteredHotels']

        for property in properties:
            information_summary = property['content']['informationSummary']
            image_urls = [f"https:{url['value'].split('?')[0]}" for img in property['content']['images']['hotelImages'] for url in img['urls'] if 'agoda' in url['value']]

            try:
                price = property['pricing']['offers'][0]['roomOffers'][0]['room']['pricing'][0]['price']['perNight']['exclusive']['display']
            except:
                price = 'Sold Out'

            hotel_info = {
                'otaPId': str(property['propertyId']),
                'Name': information_summary['displayName'],
                'Rating': information_summary.get('rating', 'N/A'),
                'Location': f"{information_summary['address']['area']['name']}, {information_summary['address']['city']['name']}",
                'Price': price,
                'ReviewSummary': {
                    'RatingScore': property['content']['reviews']['cumulative']['score'],
                    'ReviewCount': property['content']['reviews']['cumulative']['reviewCount']
                }
            }
            hotels_info.append(hotel_info)

    return total_properties, hotels_info