# encoding=utf-8
from fastdtw import fastdtw
from scipy.spatial.distance import jensenshannon
from scipy.stats import kendalltau

from GI.evaluations.utility import *
from GI.evaluations.plot import *
from GI.models.tools import ArrayConverter


class CellVisitFrequencyJSDivergence:
    """
    Calculate the Jensen–Shannon divergence between the cell visit frequency distributions of two datasets.

    Note that it is symmetric and the range is [0, 1].
    A larger value indicates a larger divergence.
    """

    @staticmethod
    def evaluate(dataset1: Dataset, dataset2: Dataset, bins: tuple):
        """
        :param dataset1: Dataset, a reference dataset, e.g., an actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param bins: tuple, some distinct cells
        :return: float
        """

        assert isinstance(dataset1, Dataset)
        assert isinstance(dataset2, Dataset)
        assert isinstance(bins, tuple)
        assert len(set(bins)) == len(bins)

        return jensenshannon(CellVisitFrequency.evaluate(dataset1, bins),
                             CellVisitFrequency.evaluate(dataset2, bins), base=2)


class CategoryVisitFrequencyJSDivergence:
    """
    Calculate the Jensen–Shannon divergence between the venue category visit frequency distributions of two datasets.

    Note that it is symmetric and the range is [0, 1].
    A larger value indicates a larger divergence.
    """

    @staticmethod
    def evaluate(dataset1: Dataset, dataset2: Dataset, bins: tuple) -> float:
        """
        :param dataset1: Dataset, a reference dataset, e.g., an actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param bins: tuple, some distinct category_ids
        :return: float
        """

        assert isinstance(dataset1, Dataset)
        assert isinstance(dataset2, Dataset)
        assert isinstance(bins, tuple)
        assert len(set(bins)) == len(bins)

        return jensenshannon(CategoryVisitFrequency.evaluate(dataset1, bins),
                             CategoryVisitFrequency.evaluate(dataset2, bins), base=2)


class DiameterDistributionJSDivergence:
    """
    Calculate the Jensen–Shannon divergence between the diameter distributions of two datasets.

    Note that it is symmetric and the range is [0, 1].
    A larger value indicates a larger divergence.
    """

    @staticmethod
    def evaluate(dataset1: Dataset, dataset2: Dataset, bins: tuple) -> float:
        """
        :param dataset1: Dataset, a reference dataset, e.g., a actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param bins: tuple, some distinct intervals
        :return: float
        """

        assert isinstance(dataset1, Dataset) and isinstance(dataset2, Dataset)
        assert isinstance(bins, tuple) and len(set(bins)) == len(bins)

        return jensenshannon(DiameterDistribution.evaluate(dataset1, bins),
                             DiameterDistribution.evaluate(dataset2, bins), base=2)


class TravelDistanceDistributionJSDivergence:
    """
    Calculate the Jensen–Shannon divergence between the travel distance distributions of two datasets.

    Note that it is symmetric and the range is [0, 1].
    A larger value indicates a larger divergence.
    """

    @staticmethod
    def evaluate(dataset1, dataset2, bins):
        """
        :param dataset1: Dataset, a reference dataset, e.g., a actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param bins: tuple, some distinct intervals
        :return: float
        """

        assert isinstance(dataset1, Dataset) and isinstance(dataset2, Dataset)
        assert isinstance(bins, tuple) and len(set(bins)) == len(bins)

        return jensenshannon(TravelDistanceDistribution.evaluate(dataset1, bins),
                             TravelDistanceDistribution.evaluate(dataset2, bins), base=2)


class TripDistributionJSDivergence:
    """
    Calculate the divergence between the trip distribution of two datatasets.

    Note that it is symmetric and the range is [0, 1].
    A larger value indicates a larger divergence.
   """

    @staticmethod
    def evaluate(dataset1: UniformGridDataset, dataset2: UniformGridDataset) -> float:
        """
        :param dataset1: Dataset, a reference dataset, e.g., a actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :return: float, a larges value indicates a larger divergence
        """

        assert isinstance(dataset1, UniformGridDataset) and isinstance(dataset2, UniformGridDataset)
        assert dataset1.grid == dataset2.grid

        cvf1 = TripDistribution.evaluate(dataset=dataset1)  # cfv is an 2D ndarray
        cvf2 = TripDistribution.evaluate(dataset=dataset2)

        return jensenshannon(cvf1.flatten(order='C'), cvf2.flatten(order='C'), base=2)


class CellPopularityKendallTau:
    """
    Calculate the 'negative' Kendall’s tau, a measure of the correspondence between
    cell visit frequencies of two datasets.

    Note that Kendall’s tau measures the correspondence between two distributions, which takes values in [-1, 1].
    A larger absolute value indicates a smaller divergence.
    """

    @staticmethod
    def evaluate(dataset1, dataset2, bins) -> float:
        """
        :param dataset1: Dataset, a reference dataset, e.g., a actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param bins: tuple, some distinct cells
        :return: float, tau
        """

        assert isinstance(dataset1, Dataset) and isinstance(dataset2, Dataset)
        assert isinstance(bins, tuple) and len(set(bins)) == len(bins)

        tau, _ = kendalltau(CellVisitFrequency.evaluate(dataset1, bins),
                            CellVisitFrequency.evaluate(dataset2, bins))
        return tau


class CircularQueryARError:
    """
    Calculate the average relative error of cirsular queries on a dataset with respect to another dataset.

    It takes values in [0, 1].
    A larger value indicates a larger divergence.
    """

    @staticmethod
    def evaluate(dataset1: Dataset, dataset2: Dataset, queries: tuple) -> float:
        """
        :param dataset1: Dataset, a reference dataset, e.g., a actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param queries: tuple, a tuple of circular queries
        :return: float, the average relative error
        """

        # to obtain the results of queries on the reference dataset
        # conduct each query on all trajectories
        results1 = [0] * len(queries)  # number of trajectories passed these queries
        for i in range(len(queries)):
            for user in dataset1.users:
                if queries[i].is_passed_through_by(user.trajectory):
                    results1[i] += 1

        # to obtain the results of queries on another dataset
        results2 = [0] * len(queries)
        for i in range(len(queries)):
            for user in dataset2.users:
                if queries[i].is_passed_through_by(user.trajectory):
                    results2[i] += 1

        # measure the relative error of pairwise query results
        errors = [0.0] * len(queries)
        # The sanity bound is used to mitigate the eﬀect of extremely selective queries.
        # An empirical value is 1% x number of trajectories in the dataset, following the 2018 CCS paper.
        sanity_bound = 0.01
        for i in range(len(queries)):
            numerator = abs(results1[i] - results2[i])
            denominator = results1[i]
            if len(dataset1.users) * sanity_bound > denominator:
                denominator = len(dataset1.users) * sanity_bound
            errors[i] = numerator / denominator

        # calculate the average
        return sum(errors) / len(queries)


class FrequentTravelPatternARError:
    """
    Calculate the average relative error of topk frequen travel patterns in a dataset with respect to another dataset.

    It takes values in [0, 1].
    A larger value indicates a larger divergence.
    """

    @staticmethod
    def evaluate(dataset1: Dataset, dataset2: Dataset, topk: int, min_len: int, max_len: int) -> float:
        """
        :param dataset1: Dataset, a reference dataset, e.g., a actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param topk: int
        :param min_len: int
        :param max_len: int
        :return: float
        """
        assert isinstance(dataset1, Dataset) and isinstance(dataset2, Dataset)
        assert isinstance(topk, int) and isinstance(min_len, int) and isinstance(max_len, int) and min_len <= max_len

        # topk most frequent travel patterns in the reference dataset
        fp_sup1 = FrequentTravelPattern.from_dataset(dataset1, min_len, max_len)
        topk_fp_sup1 = OrderedDict([fp_sup1.popitem(last=False) for _ in range(min(topk, len(fp_sup1)))])

        # topk most frequent travel patterns in another dataset
        fp_sup2 = FrequentTravelPattern.from_dataset(dataset2, min_len, max_len)
        topk_fp_sup2 = OrderedDict([fp_sup2.popitem(last=False) for _ in range(min(topk, len(fp_sup2)))])

        # calculate the relative errors
        sum_error = 0.0
        for fp1, sup1 in topk_fp_sup1.items():
            sup2 = topk_fp_sup2[fp1] if fp1 in topk_fp_sup2.keys() else 0
            sum_error += abs(sup1 - sup2) / sup1

        # take the average
        return sum_error / len(topk_fp_sup1)


class FrequentTravelPatternPrecisionRecallF1:
    """
    Calculate the precision, recall and F1 score of the similarity between the frequent travel patterns of a reference
    dataset and another dataset.

    Presicion, recall and F1 take values in [0, 1].
    A larger values indicates a smaller divergence.
    """

    @staticmethod
    def evaluate(dataset1: Dataset, dataset2: Dataset, topk: int, min_len: int, max_len: int) -> tuple:
        """
        :param dataset1: Dataset, a reference dataset, e.g., a actual dataset
        :param dataset2: Dataset, another dataset, e.g., a synthetic dataset
        :param topk: int
        :param min_len: int
        :param max_len: int
        :return: tuple, (precision, recall, f1)
        """
        assert isinstance(dataset1, Dataset) and isinstance(dataset2, Dataset)
        assert isinstance(topk, int) and isinstance(min_len, int) and isinstance(max_len, int) and min_len <= max_len

        # topk most frequent travel patterns in the reference dataset
        fp1 = tuple(FrequentTravelPattern.from_dataset(dataset1, min_len, max_len).keys())
        topk_fp1 = fp1[:min(topk, len(fp1))]

        # topk most frequent travel patterns in another dataset
        fp2 = tuple(FrequentTravelPattern.from_dataset(dataset2, min_len, max_len).keys())
        topk_fp2 = fp2[:min(topk, len(fp2))]

        # calculate the precision, recall and f1
        cnt_true_positive = 0
        for fp2 in topk_fp2:
            for fp1 in topk_fp1:
                if fp2 == fp1:
                    cnt_true_positive += 1
                    break
        precision = cnt_true_positive / len(topk_fp2)
        recall = cnt_true_positive / len(topk_fp1)
        f1 = 2 * precision * recall / (precision + recall)

        return precision, recall, f1


class TrajectoryDTWDistance:
    """
    Calculate the Dynamic Time Warping distance between two trajectories.
    """

    @staticmethod
    def evaluate(traj1: Trajectory, traj2: Trajectory) -> float:
        """
        :param traj1:
        :param traj2:
        :return:
        """

        assert isinstance(traj1, Trajectory) and isinstance(traj2, Trajectory)

        coordinates1 = np.array(checkin.location.coordinates() for checkin in traj1.checkins)
        coordinates2 = np.array(checkin.location.coordinates() for checkin in traj2.checkins)

        return fastdtw(coordinates1, coordinates2, dist=Spatial.sqeuclidean)


if __name__ == '__main__':
    def main() -> None:

        print('Loading adatrace dataset(s).')
        adatrace_directory = 'D:\\Workspace\\IWorkspace\\AdaTrace\\'
        actual_adatrace_filepath = adatrace_directory + 'brinkhoff.dat'
        actual_dataset = Dataset.import_from_adatrace(actual_adatrace_filepath)
        # pertur_adatrace_filepath = adatrace_directory + 'SYNTHETIC-DATASETS\\brinkhoff.dat-eps1.0-iteration0.dat'
        # pertur_dataset = DatasetImporter.load_adatrace(pertur_adatrace_filepath)

        # generate random geo-indistinguishable dataset
        print('Perturbe dataset(s) with GI.')
        from GI.protections.gi import GeoIndistinguishibility
        from GI.protections.epsilon import Epsilon, UniformAllocation
        pertur_dataset = GeoIndistinguishibility.perturbate(actual_dataset, Epsilon(1.0, UniformAllocation))

        # test the evaluation on the Jensen-Shannon divengence between the diameter distributions of two datasets
        bins = ArrayConverter.jenks_breaks(tuple(user.trajectory.diameter() for user in actual_dataset.users), 10)
        dd_jsd = DiameterDistributionJSDivergence.evaluate(actual_dataset, pertur_dataset, bins)
        print('Jensen-Shannon divergence of DiameterDistribution:', dd_jsd)

        # # evaluation on the Jensen-Shannon divengence between the travel distance distributions of two datasets
        # bins = ArrayConverter.jenks_breaks(tuple(user.trajectory.length() for user in actual_dataset.users), 10)
        # tdd_jsd = TravelDistanceDistributionJSDivergence.evaluate(actual_dataset, pertur_dataset, bins)
        # print('Jensen-Shannon divergence of TravelDistanceDistribution:', tdd_jsd)

        # # evaluation on the circular query error between two datasets
        # queries = CircularQuery.random_queries(actual_dataset.boundary(), 100)
        # cq_are = CircularQueryARError.evaluate(actual_dataset, pertur_dataset, queries)
        # print('CircularQueryARError:', cq_are)

        # # plot locations in the Cartesian coordinate system
        # Plot.plot_2datasets(actual_dataset, pertur_dataset)

        # # plot locations in the geographic coordinate system
        # GeoPlot.plot_dataset(actual_dataset)
        # GeoPlot.plot_dataset(pertur_dataset)

        # print('Convert to grid dataset(s).')
        # deduplication_needed = True
        # interpolation_needed = True
        # grid = UniformGrid(boundary=actual_dataset.boundary(), shape=(10, 10))
        # actual_griddataset = UniformGridDataset.as_griddataset(actual_dataset,
        #                                                        grid,
        #                                                        deduplication_needed,
        #                                                        interpolation_needed)
        # pertur_griddataset = UniformGridDataset.as_griddataset(pertur_dataset,
        #                                                        grid,
        #                                                        deduplication_needed,
        #                                                        interpolation_needed)

        # # evaluation on the Jensen-Shannon divengence between the cell visit frequencies of two datasets
        # bins = tuple(grid.cells)
        # cvf_jsd = CellVisitFrequencyJSDivergence.evaluate(actual_griddataset, pertur_griddataset, bins)
        # print('Jensen-Shannon divergence of CellVisitFrequency:', cvf_jsd)

        # # evaluation on the Jensen-Shannon divengence between the travel distributions of two datasets
        # td_jsd = TripDistributionJSDivergence.evaluate(actual_griddataset, pertur_griddataset)
        # print('Jensen-Shannon divergence of TripDistribution:', td_jsd)

        # # evaluation on the Kendall's tau between cell popularity distributions of two datasets
        # bins = tuple(grid.cells)
        # cp_kt = CellPopularityKendallTau.evaluate(actual_griddataset, pertur_griddataset, bins)
        # print('CellPopularityKendallTau:', cp_kt)

        # # evaluation on the circular query error between two datasets
        # ftp_are = FrequentTravelPatternARError.evaluate(actual_griddataset, pertur_griddataset, 10, 2, 6)
        # print('FrequentTravelPatternARError:', ftp_are)

        # # evaluation on the circular query error between two datasets
        # ftp_prf = FrequentTravelPatternPrecisionRecallF1.evaluate(actual_griddataset, pertur_griddataset, 10, 2, 6)
        # print('FrequentTravelPatternPrecisionRecallF1:', ftp_prf)


    main()
